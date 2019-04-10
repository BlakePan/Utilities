# -*- coding: utf-8 -*-
import tensorflow as tf


class TrainingThread(object):
    def __init__(self,
                 thread_index,
                 graph,
                 local_network,
                 global_network,
                 grad_applier,
                 learning_rate,
                 clip_norm,
                 train_batches,
                 trading_reward,
                 device):

        self.thread_index = thread_index
        self.local_network = local_network
        self.learning_rate = learning_rate
        self.train_batches = train_batches
        self.trading_reward = trading_reward

        local_vars = self.local_network.get_vars()
        with tf.device(device):
            self.grad_var_list = grad_applier.compute_gradients(
                self.local_network.loss, local_vars)

        # # Get gradient check target.
        # self.target_grad_var = None
        # self.target_var = None
        # for i, v in enumerate(local_vars):
        #     v_name = nn_helper.get_var_name(v.name)
        #     if v_name == params.GRAD_CHECK_TARGET:
        #         self.target_var = v
        #         self.target_grad_var = self.grad_var_list[i][0]
        #         break
        # assert self.target_grad_var != None and self.target_var != None

        # Apply gradient from local to global network.
        # dynamic gradient clipping and gradient applying
        gradients = [gv[0] for gv in self.grad_var_list]
        self.gradient_norm = tf.global_norm(gradients)
        gradient_clipped, _ = tf.clip_by_global_norm(gradients, clip_norm)
        target_grad_var_list = zip(gradient_clipped, global_network.get_vars())
        self.sync = self.local_network.sync_from(global_network)

        # For using batch normalization.
        # https://www.tensorflow.org/versions/r0.12/api_docs/python/contrib.layers/higher_level_ops_for_building_neural_network_layers_#batch_norm
        with graph.as_default():
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS, scope=self.local_network.get_scope())
        with tf.control_dependencies(update_ops):
            # Ensure that we execute the update_ops before performing the train_step
            self.apply_gradients = grad_applier.apply_gradients(target_grad_var_list)

    def train_step(self, sess, input_batch, importance_sampling):

        # Prepare input.
        data_batch, idx_batch = input_batch
        x_batch, s_batch, z_batch, steps_batch, trends_label_batch, trends_acc_z_batch = zip(*data_batch)
        feed_dict = {
            self.local_network.input_x: x_batch,
            self.local_network.input_s: s_batch,
            self.local_network.input_z: z_batch,
            self.local_network.input_steps: steps_batch,
            self.local_network.input_trends_label: trends_label_batch,
            self.local_network.input_trends_acc_z: trends_acc_z_batch,
            self.local_network.importance_sampling: importance_sampling,
            self.local_network.is_training: True
        }

        _, trading_loss, trend_loss, trend_accuracy, gradient_norm, target_grad_val, \
        batch_Rts, delta_ts, needs_training, delta_ts_error_pos, delta_ts_error_neg = sess.run(
            [self.apply_gradients, self.local_network.trading_loss, self.local_network.trend_loss,
             self.local_network.trend_accuracy, self.gradient_norm, self.target_grad_var,
             self.local_network.batch_Rts, self.local_network.delta_ts, self.local_network.delta_ts_needs_training,
             self.local_network.delta_ts_error_pos, self.local_network.delta_ts_error_neg],
            feed_dict)

        # logging.info("[train_step] trading loss {:g}, trend_loss {:g}".format(trading_loss, trend_loss))
        # logging.info("[train_step] Rts_raw {}".format(Rts_raw))
        # logging.info("[train_step] Rts_raw_acc {}".format(Rts_raw_acc))
        # logging.info("[train_step] delta_ts {}".format(delta_ts))
        # logging.info("[train_step] delta_ts > 0: {} < 0: {}, needs_training {}".format((delta_ts > 0).sum(), (delta_ts < 0).sum(), (Rts_raw_acc_needs_training != 0.0).sum()))

        for i, idx in enumerate(idx_batch):
            self.trading_reward[idx] = batch_Rts[i]

        return trading_loss, trend_loss, trend_accuracy, gradient_norm, target_grad_val, delta_ts, (
                    needs_training != 0.0).sum(), \
               (delta_ts_error_pos != 0.0).sum(), (delta_ts_error_neg != 0.0).sum()

    def process(self, sess, importance_sampling_params, q_l2g, q_g2l):

        # parameters of prioritized experience replay and importance sampling
        num_samples, segment_numbers, beta, beta_step = importance_sampling_params

        current_step = 0
        trading_loss_sum = 0.0
        trend_loss_sum = 0.0
        trend_accuracy_sum = 0.0
        gradient_norm_sum = 0.0
        delta_ts_pos = 0
        delta_ts_discrete_pos = 0
        delta_ts_neg = 0
        delta_ts_discrete_neg = 0
        needs_training_cnt = 0
        delta_ts_error_pos_cnt = 0
        delta_ts_error_neg_cnt = 0
        for input_batch in self.train_batches:

            # Synchronize with the global network.
            sess.run(self.sync)

            # Update importance_sampling.
            beta += beta_step
            importance_sampling = np.array([pow(n / num_samples, beta) for n in segment_numbers])
            importance_sampling = importance_sampling / np.amax(importance_sampling)

            trading_loss, trend_loss, trend_accuracy, gradient_norm, target_grad_val, delta_ts, needs_training, delta_ts_error_pos, delta_ts_error_neg = self.train_step(
                sess, input_batch, importance_sampling)

            current_step += 1
            trading_loss_sum += trading_loss
            trend_loss_sum += trend_loss
            trend_accuracy_sum += trend_accuracy
            gradient_norm_sum += gradient_norm
            delta_ts_pos += (delta_ts > 0).sum()
            delta_ts_discrete_pos += (delta_ts > params.DISCRETIZE_POLICY_THRESHOLD).sum()
            delta_ts_neg += (delta_ts < 0).sum()
            delta_ts_discrete_neg += (delta_ts < -params.DISCRETIZE_POLICY_THRESHOLD).sum()
            needs_training_cnt += needs_training
            delta_ts_error_pos_cnt += delta_ts_error_pos
            delta_ts_error_neg_cnt += delta_ts_error_neg
            if current_step % params.EVALUATE_EVERY == 0:
                # gradient check
                target_val, lr = sess.run([self.target_var, self.learning_rate])
                param_scale = np.linalg.norm(target_val.ravel())
                update = -lr * target_grad_val
                update_scale = np.linalg.norm(update.ravel())
                grad_check_ratio = float(update_scale / param_scale)

                # Send the training information.
                trading_loss_avg = trading_loss_sum / params.EVALUATE_EVERY
                trend_loss_avg = trend_loss_sum / params.EVALUATE_EVERY
                trend_accuracy_avg = trend_accuracy_sum / params.EVALUATE_EVERY
                gradient_norm_avg = gradient_norm_sum / params.EVALUATE_EVERY
                delta_ts_num = params.EVALUATE_EVERY * delta_ts.size
                delta_ts_pos_avg = delta_ts_pos / delta_ts_num
                delta_ts_discrete_pos_avg = delta_ts_discrete_pos / delta_ts_num
                delta_ts_neg_avg = delta_ts_neg / delta_ts_num
                delta_ts_discrete_neg_avg = delta_ts_discrete_neg / delta_ts_num
                needs_training_avg = needs_training_cnt / delta_ts_num
                delta_ts_error_pos_avg = delta_ts_error_pos_cnt / delta_ts_num
                delta_ts_error_neg_avg = delta_ts_error_neg_cnt / delta_ts_num
                q_l2g.put(("train_info", trading_loss_avg, trend_loss_avg, trend_accuracy_avg, gradient_norm_avg,
                           grad_check_ratio, delta_ts_pos_avg, delta_ts_discrete_pos_avg, delta_ts_neg_avg,
                           delta_ts_discrete_neg_avg, needs_training_avg, delta_ts_error_pos_avg,
                           delta_ts_error_neg_avg))

                # Reset statistics.
                trading_loss_sum = 0.0
                trend_loss_sum = 0.0
                trend_accuracy_sum = 0.0
                gradient_norm_sum = 0.0
                delta_ts_pos = 0
                delta_ts_discrete_pos = 0
                delta_ts_neg = 0
                delta_ts_discrete_neg = 0
                needs_training_cnt = 0
                delta_ts_error_pos_cnt = 0
                delta_ts_error_neg_cnt = 0

            # Check the message queue from main thread.
            try:
                msg = q_g2l.get(block=False)
                if msg == "terminate":
                    break
                else:
                    assert False, "Invalid msg {}".format(msg)
            except queue.Empty:
                pass

        # end of training
        q_l2g.put(("eot",))
