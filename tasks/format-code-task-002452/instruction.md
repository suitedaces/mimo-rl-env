# Problem Statement

我用 cf_writer 存数据的时候发现，地理坐标（lat/lon）的 area 写出来的 netCDF 不太对，x、y 坐标的 standard_name 居然是 projection_x_coordinate / projection_y_coordinate，units 还是 m。但我这明明是经纬度的数据，不应该是 longitude/latitude、degrees_east/degrees_north 吗？这样写出来的文件感觉不符合 CF 规范。能不能根据 area 的 CRS 自动判断一下，如果是地理坐标就用度数那套？投影坐标的还是保持原样就行。

# Expected outcomes

- For data saved through the CF writer with a geographic latitude/longitude area, the written `x` coordinate metadata identifies it as longitude and uses east-positive degree units.
- For data saved through the CF writer with a geographic latitude/longitude area, the written `y` coordinate metadata identifies it as latitude and uses north-positive degree units.
- For data saved through the CF writer with a projected area, the written `x` and `y` coordinate metadata continues to use projected coordinate names and metre units.
- The coordinate metadata choice should be driven by the coordinate reference system associated with the data when that information is available, without adding unintended coordinate metadata to the final CF output.
- When the writer cannot confidently classify the coordinate reference information, it should remain compatible with the previous projected-coordinate behavior and report the ambiguity rather than failing unexpectedly.

# Implementation notes

- The exact internal structure, helper functions, and validation location are up to the implementer.
- Preserve existing CF writer behavior for projected-coordinate data while adding correct handling for geographic latitude/longitude areas.
- Prefer externally observable CF output semantics over changes tied to a specific internal code path.
