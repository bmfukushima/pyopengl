from OpenGL.GL import *

from .mesh import Mesh

class Renderer(object):

    def __init__(self, clear_color=[0, 0, 0]):
        glEnable(GL_DEPTH_TEST)
        glClearColor(*clear_color)

    def render(self, scene, camera):
        # clear buffers
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)

        # update camera view matrix
        camera.updateViewMatrix()

        # get mesh objects
        descendents = scene.getDescendentList()

        # lambdas are just one line functions
        ## lambda <function args> : return <this>
        ## lambda x : x + 1
        ##
        mesh_filter = lambda x : isinstance(x, Mesh)
        mesh_list = list(filter(mesh_filter, descendents))

        for mesh in mesh_list:
            # visible
            if not mesh.visible:
                continue

            # init mesh program
            glUseProgram(mesh.material.program)

            # bind mesh vao
            glBindVertexArray(mesh.vao)

            # update uniform matrices



