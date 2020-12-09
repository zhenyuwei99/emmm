
from emmm.core.molecule import Molecule
from emmm.core.atom import Atom

import numpy as np
from emmm.core.adt import Item


class Bioperate:

    @staticmethod
    def seperate(item1:Item, item2:Item, type:str, value:float):
        """ [In-place] to separate two items in opposite direction
            relative distance is move EACH item in a distance under system unit; absolute distance is the time of current distance of two items
            e.g.:
            item1+=unit_orientation_vector*relative
            item1+=orientation*abusolute

        Args:
            item1 (Item): Atom|Molecule
            item2 (Item): Atom|Molecule
            type (str): relative|absolute distance
            value (float): vale
        """
        coords1 = item1.coords
        coords2 = item2.coords

        # orientation vector 
        oriVec = coords2 - coords1
        uniVec = oriVec/np.linalg.norm(oriVec)

        if type=='relative' or type=='rel':
            coords2 += uniVec*value
            coords1 -= uniVec*value
        if type=='abusolute' or type=='abs':
            coords2 += oriVec*value
            coords1 -= oriVec*value

        item1.coords = coords1
        item2.coords = coords2

    @staticmethod
    def distance(item1:Item, item2:Item)->float:
        """[Return] measure the distance between two items  

        Args:
            item1 (Item): Atom|Molecule
            item2 (Item): Atom|Molecule

        Returns:
            distance (Float)
        """
        dist = 0   

        coords1 = item1.coords
        coords2 = item2.coords

        dist = np.linalg.norm(coords2-coords1, ord=2)

        return dist

class Unioperate:

    @staticmethod
    def move(item:Item, x:float, y:float, z:float):
        """[In-place] move a item
        """
        vec = np.array([x,y,z], dtype=float)
        item.coords += vec
        
    @staticmethod
    def randmove(item:Item, distance:float):
        """[In-place] move a item by the length

        Args:
            item (Item): Atom|Molecule
            distance (Float): distance in float
        """
        vec =  np.random.random([3, 1])
        vec /= np.linalg.norm(vec)
        vec *= distance
        item.coords += vec

    @staticmethod
    def rotate(item:Item, theta, x, y, z, x0=0, y0=0, z0=0):
        """[In-place] rotate an item around an rotation axis which defined by (x-x0,y-y0,z-z0).

        Args:
            item (Item): Atom|Molecule
            theta (radian): theta:=theta*PI
            x (float): head of vector
            y (float): head of vector
            z (float): head of vector
            x0 (float): tail of vector
            y0 (float): tail of vector
            z0 (float): tail of vector
        Returns:
            [type]: [description]
        """
        # rotation axis
        disVec = np.array([x0, y0, z0],dtype=float)
        rotax = np.array([x,y,z], dtype=float)- disVec

        rotax = rotax/ np.linalg.norm(rotax)
        rotaxX, rotaxY, rotaxZ = rotax

        # half theta = theta/2
        theta = np.pi*theta

        stheta = np.sin(theta/2)

        a = np.cos(theta/2)
        b = stheta*rotaxX
        c = stheta*rotaxY
        d = stheta*rotaxZ
        b2 = b**2
        c2 = c**2
        d2 = d**2
        ab = a*b
        ac = a*c
        ad = a*d
        bc = b*c
        bd = b*d
        cd = c*d

        # rotation matrix
        rotm = np.array([[1-2*(c2+d2), 2*(bc-ad), 2*(ac+bd)],
                         [2*(bc+ad), 1-2*(b2+d2), 2*(cd-ab)],
                         [2*(bd-ac), 2*(ab+cd), 1-2*(b2+c2)]])

        item.coords -= disVec
        item.coords = np.dot(rotm, item)
        item.coords += disVec

    @staticmethod
    def rotate_orth(item, theta, x, y, z, xAxis, yAxis, zAxis):

        Unioperate.rotate(item, theta, x+xAxis, y+yAxis, z+zAxis, x, y, z)

    @staticmethod
    def calc_centroid(item:Molecule):
        
        if isinstance(item, Atom):
            print('Warning: we dont talk about a centroid of an atom')
        else:
            atoms = item.flatten()
            vec = np.array([0,0,0])
            for atom in atoms:
                vec+=atom.coords

            centroid = vec/len(atoms)
            setattr(item, 'centroid', centroid)

