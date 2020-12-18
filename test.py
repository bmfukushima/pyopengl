from core.base import Base

class Test(Base):
    def initialize(self):
        print ("Hello PyGame")

    def update(self):
        pass

if __name__ == "__main__":
    Test().run()