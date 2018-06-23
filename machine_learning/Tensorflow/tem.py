
import tensorflow as tf
import numpy as np
#import input_data
#mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

x1=tf.placeholder(tf.int32,shape=[1],name='x1')
x2=tf.constant(2, name='x2')
c=x1+x2


with tf.Session() as sess:
    result=sess.run(c,{x1:[3]})
    print(result)

# 使用 NumPy 生成假数据(phony data), 总共 100 个点.
x_data = np.float32(np.random.rand(2, 100)) # 随机输入
y_data = np.dot([0.100, 0.200], x_data) + 0.300


import tensorflow.examples.tutorials.mnist.input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


