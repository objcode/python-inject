#Inject python locals#


A bit of hackery to experiment with alternative call flow in python.

To use:

    def foo():
        print a
       
    inject(a=5).into(foo)
    >> 5

    @inject(cat='man')
    def bar():
        print "the cat is a", cat

    bar()
    >> the cat is a man


**Q:  Why should I use this?**

A: You shouldn't

**Q: Why does it exist?**

A: Because it can

**Q: Are you crazy?**

A: ?

**Q: Is it good?**

A: yes
