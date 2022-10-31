# Plan

When your manager asks you to build an ERP and you have only Excel...

***
Long, long time ago on a plant that does not already exist, we had to plan a production of thousands of parts and 
units. We had no money for a good ERP soft. But we had Excel and the process was absolutely painful. 
Scheduling had taken us too much time. So, I decided to try python to solve that problem. I just started 
programming, so, the first version of this ERP based on python was ugly. Well, ok, it's still ugly :) Now I want to 
introduce you the api for this ERP system.

***
There are several types of entities inside this ERP system. And now it is time to speak about them.

### Part
It's a small and simple component of the final product. Screw, nut and so on. It doesn't contain any other elements 
inside it. But it could have a very complex route through the plant. Especially if we need to perform chemical 
processing several times.

### Unit
This is a component, that may include parts and other units. Imagine a pen: it has stem and body, which are parts, 
and the pen is a sort of unit in this case (actually, final product, but doesn't matter).

### Operation
To build a final product we need to unite parts and units step by step, operation by operation. Different operations 
may use the same parts and units.

### Product
Well, this is the simplest part, you may think. But no. On our plant we had just a few models of final product, but 
every model had its own versions - for each customer. Anyway, to build s product, we planned operations. To perform 
operations we planned parts and units.

### Section
As I said earlier, every part and unit has its own rout through the plant. Section is just another point on the route. 
We planned the production parts and units for each section on the route except the last point (because it's a consumer 
point).

***
You cannot plan without accounting. This ERP system includes an accounting module. When the part or unit passed 
a section, we added this information to the database and got a valid state of remnants.

### How to use?

This is a backend part of the ERP system. It is implemented as api with swagger documentation. To launch the service:
```bash 
make build
```

Docker should be installed, ofcourse.
