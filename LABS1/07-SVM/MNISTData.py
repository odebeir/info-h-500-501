# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Functions for downloading and reading MNIST data."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import gzip
import os
import numpy
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin

SOURCE_URL = 'http://yann.lecun.com/exdb/mnist/'

def maybe_download(filename, work_directory):
    """Download the data from Yann's website, unless it's already here."""
    if not os.path.exists(work_directory):
        os.mkdir(work_directory)
    filepath = os.path.join(work_directory, filename)
    if not os.path.exists(filepath):
        filepath, _ = urllib.request.urlretrieve(SOURCE_URL + filename, filepath)
        statinfo = os.stat(filepath)
        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
    return filepath

def _read32(bytestream):
    dt = numpy.dtype(numpy.uint32).newbyteorder('>')
    return numpy.frombuffer(bytestream.read(4), dtype=dt)[0]

def extract_images(filename):
    """Extract the images into a 4D uint8 numpy array [index, y, x, depth]."""
    print('Extracting', filename)
    with gzip.open(filename) as bytestream:
        magic = _read32(bytestream)
        if magic != 2051:
            raise ValueError('Invalid magic number %d in MNIST image file: %s' % (magic, filename))
        num_images = _read32(bytestream)
        rows = _read32(bytestream)
        cols = _read32(bytestream)
        buf = bytestream.read(rows * cols * num_images)
        data = numpy.frombuffer(buf, dtype=numpy.uint8)
        data = data.reshape(num_images, rows, cols, 1)
        return data

def dense_to_one_hot(labels_dense, num_classes=10):
    """Convert class labels from scalars to one-hot vectors."""
    num_labels = labels_dense.shape[0]
    index_offset = numpy.arange(num_labels) * num_classes
    labels_one_hot = numpy.zeros((num_labels, num_classes))
    labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
    return labels_one_hot

def extract_labels(filename, one_hot=False):
    """Extract the labels into a 1D uint8 numpy array [index]."""
    print('Extracting', filename)
    with gzip.open(filename) as bytestream:
        magic = _read32(bytestream)
        if magic != 2049:
            raise ValueError('Invalid magic number %d in MNIST label file: %s' % (magic, filename))
        num_items = _read32(bytestream)
        buf = bytestream.read(num_items)
        labels = numpy.frombuffer(buf, dtype=numpy.uint8)
        if one_hot:
            return dense_to_one_hot(labels)
        return labels


class MNISTData(object):
    
    def __init__(self, **kwargs):  
        self.train_dir = kwargs['train_dir'] if 'train_dir' in kwargs else None
        one_hot = kwargs['one_hot'] if 'one_hot' in kwargs else False

        TRAIN_IMAGES = 'train-images-idx3-ubyte.gz'
        TRAIN_LABELS = 'train-labels-idx1-ubyte.gz'
        TEST_IMAGES = 't10k-images-idx3-ubyte.gz'
        TEST_LABELS = 't10k-labels-idx1-ubyte.gz'
        VALIDATION_SIZE = 5000
        local_file = maybe_download(TRAIN_IMAGES, self.train_dir)
        train_images = extract_images(local_file)
        local_file = maybe_download(TRAIN_LABELS, self.train_dir)
        train_labels = extract_labels(local_file, one_hot=one_hot)
        local_file = maybe_download(TEST_IMAGES, self.train_dir)
        test_images = extract_images(local_file)
        local_file = maybe_download(TEST_LABELS, self.train_dir)
        test_labels = extract_labels(local_file, one_hot=one_hot)
        validation_images = train_images[:VALIDATION_SIZE]
        validation_labels = train_labels[:VALIDATION_SIZE]
        train_images = train_images[VALIDATION_SIZE:]
        train_labels = train_labels[VALIDATION_SIZE:]
        self.train = self.setup(images=train_images, labels=train_labels)
        self.validation = self.setup(images=validation_images, labels=validation_labels)
        self.test = self.setup(images=test_images, labels=test_labels)
        
        self.initialized = True

    def setup(self, **kwargs):
        assert ('images' in kwargs and 'labels' in kwargs), "images and labels arguments must be provided."

        images = kwargs['images']
        labels = kwargs['labels']
        assert images.shape[0] == labels.shape[0], ('images.shape: %s labels.shape: %s' % (images.shape,labels.shape))
        
        dic = {}

        dic['num_examples'] = images.shape[0]
        # Convert shape from [num examples, rows, columns, depth]
        # to [num examples, rows*columns] (assuming depth == 1)
        assert images.shape[3] == 1
        images = images.reshape(images.shape[0],images.shape[1] * images.shape[2])
        # Convert from [0, 255] -> [0.0, 1.0].
        images = images.astype(numpy.float32)
        images = numpy.multiply(images, 1.0 / 255.0)
        dic['images'] = images
        dic['labels'] = labels
        dic['epochs_completed'] = 0
        dic['index_in_epoch'] = 0
        return dic

    def next_batch(self, n, **kwargs):
        dataset = kwargs['set'] if 'set' in kwargs else self.train

        """Return the next `n` examples from this data set."""
        start = dataset['index_in_epoch']
        dataset['index_in_epoch'] += n
        if dataset['index_in_epoch'] > dataset['num_examples']:
            # Finished epoch
            dataset['epochs_completed'] += 1
            # Shuffle the data
            perm = numpy.arange(dataset['num_examples'])
            numpy.random.shuffle(perm)
            dataset['images'] = dataset['images'][perm]
            dataset['labels'] = dataset['labels'][perm]
            # Start next epoch
            start = 0
            dataset['index_in_epoch'] = n
            assert n <= dataset['num_examples']
        end = dataset['index_in_epoch']
        return dataset['images'][start:end], dataset['labels'][start:end]

    def get_inputshape(self):
        return [784]