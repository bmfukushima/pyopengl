"""
private     :- / :>
is  a       -->
has a       |>

geometry
    :> Geometry --> object
    |> Rectangle --> Geometry
    |> Cube --> Geometry
material
    :> AbstractMaterial --> object
    |> LineMaterial --> MainMaterial
    |> MainMaterial --> AbstractMaterial
    |> MeshMaterial --> MainMaterial
    |> PointMaterial --> MainMaterial

object
    :> Object3D --> object
    |> Camera --> Object3D
    |> Group --> Object3D
    |> Mesh --> Object3D
    |> Scene --> Object3D
utils
    |> Attribute
    |> Matrix
    |> ObjectArray
    |> Uniform
    |> Utils

"""