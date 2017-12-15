import cv2
#import PyNet as net
from proj4AdetectFace import detectFace
from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull
from proj2helpers import calculateAFromIdx, get_rgb
import numpy as np
from facialLandmark import facialLandmark
import sys
#from getConvexHull import getConvexHull

# img1 and img2 are nxn numpy matricies
# noinspection PyInterpreter
def faceReplacement(img1, img2):

    #do face detection and get bounding boxes
    #returns numFacesx4x2 where 4 is four corners and 3rd dimension is xy
    bboxImg1 = detectFace(img1)
    bboxImg2 = detectFace(img2)

    #get facial landmarks from the PyNet CNN
    #returns nx2 locations of the features
    # myModel = net.Model.load_model("Project4BCNN/500.pickle")
    # landmarksImg1 = myModel.forward(img1)
    # landmarksImg2 = myModel.forward(img2)

    #get facial landmarks from dlibs
    #nx2 each
    landmarksImg1 = facialLandmark(img1)
    landmarksImg2 = facialLandmark(img2)

    print (landmarksImg1.shape, landmarksImg2.shape)
    
    # #getRGB image
    # img1_gray = rgb2gray(img1)
    # img2_gray = rgb2gray(img2)
    #
    # #get the facial features for the image
    # #returns 250xnumFaces points for x locations and y locations
    # xFeatures1, yFeatures1 = getFeatures(img1_gray, bboxImg1)
    # features1 = np.hstack((xFeatures1,yFeatures1))
    # xFeatures2, yFeatures2 = getFeatures(img2_gray, bboxImg2)
    # features2 = np.hstack((xFeatures2,yFeatures2))
    #
    # #get the two convex hulls for the images
    # convexHull1 = cv2.convexHull(features1, returnPoints=True)
    # convexHull2 = cv2.convexHull(features2, returnPoints=True)

    #get the triangulations
    tri1 = Delaunay(landmarksImg1)
    tri2 = Delaunay(landmarksImg2)

    #get the convex hulls
    hull1 = ConvexHull(landmarksImg1)
    hull2 = ConvexHull(landmarksImg2)

    #plot the image
    #plt.imshow(img1)
    #plot the triangulation
    #plt.triplot(landmarksImg1[:, 0], landmarksImg1[:, 1], tri1.simplices.copy())
    #plot the hull
    #plt.plot(landmarksImg1[hull1.vertices, 0], landmarksImg1[hull1.vertices, 1], 'r--', lw=2)
    #plt.show()

    #append the facial landmarks and the convexhulls together
    img1Features = np.vstack((landmarksImg1,hull1.points[hull1.vertices]))
    img2Features = np.vstack((landmarksImg2,hull2.points[hull2.vertices]))

    #make sure features same size
    minPts = np.min([img1Features.shape[0],img2Features.shape[0]])
    img1Features = img1Features[0:minPts,:]
    img2Features = img2Features[0:minPts,:]

    #create delanuy triangulation
    tri1 = Delaunay(img1Features).simplices
    tri2 = Delaunay(img2Features).simplices

    [numTriangles1,_,] = tri1.shape
    [numTriangles2,_,] = tri2.shape

    #print (numTriangles1, numTriangles2)

    #img2 = 255 * np.ones(img_in.shape, dtype=img_in.dtype)

    #do the warping for each of the triangles
    for triangle in range(0,numTriangles):
        srcTriangle = tri1[triangle,:]
        destTriangle = tri2[triangle,:]

        r1 = cv2.boundingRect(srcTriangle)
        r2 = cv2.boundingRect(destTriangle)

    #do affine warp of the triangles

    #find transform for eachTriangle
    simplices1 = tri1.simplices
    simplices2 = tri2.simplices

    #allocate memory
    loAffineTransforms12 = np.zeros((len(simplices1), 2, 3)) #store affine for 1 -> 2
    loAffineTransforms21 = np.zeros((len(simplices1), 2, 3)) #store affine for 2 -> 1
    pts1 = np.zeros((3,2))
    pts2 = np.zeros((3,2))

    #calculate transform for each triangle in both directions
    for i in range(len(simplices1)):
        pts1[0] = img1Features[simplices1[i][0]]
        pts1[1] = img1Features[simplices1[i][1]]
        pts1[2] = img1Features[simplices1[i][2]]

        pts2[0] = img2Features[simplices2[i][0]]
        pts2[1] = img2Features[simplices2[i][1]]
        pts2[2] = img2Features[simplices2[i][2]]

        loAffineTransforms12[i] = cv2.AffineTransform(pts1, pts2)
        loAffineTransforms21[i] = cv2.AffineTransform(pts1, pts2)

    #warp each triangle
    for i in range(len(simplices1)):
        #get points for rect
        pts1[0] = img1Features[simplices1[i][0]]
        pts1[1] = img1Features[simplices1[i][1]]
        pts1[2] = img1Features[simplices1[i][2]]
        
        x,y,w,h = cv2.boundingRect(pts) 
        
        
    #blending if want to
    #we can call this function
    #output = cv2.seamlessClone(src, dst, mask, center, cv2.NORMAL_CLONE)


    return [img1Warped, img2Warped]