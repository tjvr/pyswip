# -*- coding: utf-8 -*-


# pyswip -- Python SWI-Prolog bridge
# Copyright (c) 2007-2012 Yüce Tekol
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#  
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#  
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Run several complex examples using pySwip. The main goal of these tests is
ensure stability in several platforms.
"""


import unittest

from pyswip import *


class TestExamples(unittest.TestCase):
    """
    Each test method is named after one example in $PYSWIP/examples.

    To avoid complexities related to finding the example directory, all the
    examples are copied as tests here.

    WARNING: Since it is not possible to unload things from the Prolog base, the
    examples have to be 'orthogonal'.
    
    """

    def test_create_term(self):
        """
        Simple example of term creation.
        """
        
        prolog = Prolog()
    
        a1 = PL_new_term_refs(2)
        a2 = a1 + 1
        t = PL_new_term_ref()
        ta = PL_new_term_ref()
 
        animal2 = PL_new_functor(PL_new_atom("animal"), 2)
        assertz = PL_new_functor(PL_new_atom("assertz"), 1)
 
        PL_put_atom_chars(a1, "gnu")
        PL_put_integer(a2, 50)
        PL_cons_functor_v(t, animal2, a1)
        PL_cons_functor_v(ta, assertz, t)
        PL_call(ta, None)
    
        result = list(prolog.query("animal(X,Y)", catcherrors=True))
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0], {'X': 'gnu', 'Y': 50})


    def test_knowledgebase(self):
        """
        Tests usage of modules.
        """

        p = Prolog()
         
        assertz = Functor("assertz")
        parent = Functor("parent", 2)
        test1 = newModule("test1")
        test2 = newModule("test2")
         
        call(assertz(parent("john", "bob")), module=test1)
        call(assertz(parent("jane", "bob")), module=test1)
         
        call(assertz(parent("mike", "bob")), module=test2)
        call(assertz(parent("gina", "bob")), module=test2)
         
        # Test knowledgebase module test1
 
        result = set()
        X = Variable()
        q = Query(parent(X, "bob"), module=test1)
        while q.nextSolution():
            result.add(X.value.value)    # X.value is an Atom
        q.closeQuery()
        self.assertEquals(result, set(["john", "jane"]))
         
        # Test knowledgebase module test2
         
        result = set()
        q = Query(parent(X, "bob"), module=test2)
        while q.nextSolution():
            result.add(X.value.value)
        q.closeQuery()
        self.assertEquals(result, set(["mike", "gina"]))

    def test_father(self):
        """
        Tests basic inferences.
        """

        p = Prolog()
     
        father = Functor("father", 2)
        mother = Functor("mother", 2)
     
        p.assertz("father(john,mich)")
        p.assertz("father(john,gina)")
        p.assertz("mother(jane,mich)")
     
        X = Variable()
        Y = Variable()
        Z = Variable()
  
        result = []
        q = Query(father("john", Y), mother(Z, Y))
        while q.nextSolution():
            y = Y.value.value
            z = Z.value.value
            result.append({'Y': y, 'Z': z})
        q.closeQuery()
   
        # FIXME: For some reason, when using Query the iterator is repeating
        # solutions
#        self.assertEquals(len(result), 1)
#        self.assertEquals(result[0], {'Y': 'mich', 'Z': 'jane'})

        # Repeat the same query but using strings
        result = []
        for s in p.query("father(john,Y),mother(Z,Y)"):
            result.append(s)
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0], {'Y': 'mich', 'Z': 'jane'})
     
    def test_coins(self):
        """
        Runs the coins example (uses clp library of SWI-Prolog).
        """
        
        prolog = Prolog()
        prolog.consult("coins.pl")
        count = 100
        total = 500
        coins = Functor("coins", 3)
        S = Variable()
        q = Query(coins(S, count, total))
 
        solutions = []
        while q.nextSolution():
            solutions.append(S.value)
        q.closeQuery()
 
        self.assertEquals(len(solutions), 105)

     # FIXME: This example is always segfaulting. Deactivated until solved. The
     # reason is probably on the other tests
#    def test_draughts(self):
#        """
#        Runs the draughts example (uses clp library of SWI-Prolog).
#        """
#        
#        prolog = Prolog()
#        prolog.consult("draughts.pl")
#        solutions = []
#        for soln in prolog.query("solve(B)."):
#            solutions.append(soln["B"])
#        self.assertEquals(len(solutions), 37)

     # FIXME: This example is always segfaulting. Deactivated until solved
#    def test_hanoi(self):
#        """
#        Runs the hanoi example.
#        """
# 
#        N = 3  # Number of disks
# 
#        result = []
#        def notify(t):
#            result.append((t[0].value, t[1].value))
#        notify.arity = 1
# 
#        prolog = Prolog()
#        registerForeign(notify)
#        prolog.consult("hanoi.pl")
#        list(prolog.query("hanoi(%d)" % N)) # Forces the query to run completely
# 
#        self.assertEquals(len(result), 7)
#        self.assertEquals(result[0], ('left', 'right'))
#        self.assertEquals(result[1], ('left', 'center'))
#        self.assertEquals(result[2], ('right', 'center'))
        
        

if __name__ == "__main__":
    unittest.main()
    
