### Missing wrapper for `cv::minEnclosingCircle`

I'm using gocv to analyse contours from `FindContours` and I need to compute the smallest circle that encloses each contour (OpenCV's `cv::minEnclosingCircle`). gocv already exposes `MinAreaRect` for the rotated bounding rectangle, but I can't find an equivalent for the minimum enclosing circle anywhere in the package.

For my use case (detecting roughly circular objects and measuring their radius), the rotated rectangle isn't a good fit — I really want the circle that the OpenCV function returns, including its center and radius.

Reference to the OpenCV function:
https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga8ce13c24081bbc7151e9326f412190f1

Could a binding for `minEnclosingCircle` be added so it can be called on a `[]image.Point` like `MinAreaRect` is?
