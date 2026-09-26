I want the mysql2rgeo adapter to expose a pure Arel expression method `st_distance_sphere(rhs, units = nil)` on spatial Arel expressions, including table attributes such as `Place.arel_table[:lonlat]`, constants created with `Arel.spatial(rgeo_geometry)`, and spatial function nodes returned by other Arel spatial methods.

Calling `Place.arel_table[:lonlat].st_distance_sphere("SRID=4326;POINT(-72.099 42.099)")` should return an `RGeo::ActiveRecord::SpatialNamedFunction` named `ST_Distance_Sphere` with the receiver and RHS as its two expressions, so it can be used in predicates like `.lt(500)` inside ActiveRecord `where` clauses and serialize as a MySQL `ST_Distance_Sphere(...)` call with both geometry arguments handled as spatial values.

Calling `Place.arel_table[:lonlat].st_distance_sphere(other_geom, :meter)` should return the same kind of Arel node with a third expression equal to the string `"meter"`; that units argument should be a normal non-spatial argument while the receiver and RHS remain spatial arguments.

The method should be referentially transparent: repeated calls with the same receiver, RHS, and units produce equivalent Arel nodes, and it must not mutate the receiver, the RHS string or geometry object, database state, filesystem, network, or global ActiveRecord configuration.
