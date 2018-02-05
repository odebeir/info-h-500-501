import matplotlib.pyplot as plt

def compare(f,g,roi=None):
    plt.figure(figsize=[10,10])
    plt.subplot(1,2,1)
    plt.imshow(f,cmap=plt.cm.gray)
    plt.gca().invert_yaxis()
    plt.subplot(1,2,2)
    plt.imshow(g,cmap=plt.cm.gray)
    plt.gca().invert_yaxis()
    if roi is not None:
        f = f[roi[0]:roi[1],roi[2]:roi[3]]
        g = g[roi[0]:roi[1],roi[2]:roi[3]]
        plt.figure(figsize=[10,10])
        plt.subplot(1,2,1)
        plt.imshow(f,cmap=plt.cm.gray)
        plt.gca().invert_yaxis()
        plt.subplot(1,2,2)
        plt.imshow(g,cmap=plt.cm.gray)
        plt.gca().invert_yaxis()