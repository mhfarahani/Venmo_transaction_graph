# Table of Contents

1. [Summary] (README.md#challenge-summary)
2. [Details of Implementation] (README.md#details-of-implementation)


For this coding challenge, you will develop tools that could help analyze Venmo’s dataset. Some of the challenges here mimic real world problems.


##Summary

[Back to Table of Contents] (README.md#table-of-contents)

This code uses Venmo payments that stream in to build a  graph of users and their relationship with one another. It outputs the median degree of a vertex in a graph and update this each time a new Venmo payment appears. The median degree reoprted across a T-second sliding window (defult T = 60-second).

The vertices on the graph represent Venmo users and whenever one user pays another user, an edge is formed between the two users.

The source code uses the following python packages:

* **sys** 

* **json** 

* **datetime** 

* **time** 

* **heapq**

* **numpy**

##Details of implementation

[Back to Table of Contents] (README.md#table-of-contents)

Normally, payments can be obtained through Venmo’s API, but here we assume this has already been done, and data has been written to a file named `venmo-trans.txt` in a directory called `venmo_input`.

This file `venmo-trans.txt` contains the actual JSON messages with each payment on a newline:

`venmo-trans.txt`:

	{JSON of first payment}  
	{JSON of second payment}  
	{JSON of third payment}  
	.
	.
	.
	{JSON of last payment}  
 
One example of the data for a single Venmo payment might look like:

<pre>
{"created_time": "2014-03-27T04:28:20Z", "target": "Jamie-Korn", "actor": "Jordan-Gruber"}
</pre>

The code updates the graph and its associated median degree each time a new payment is processed. The graph only consist of payments with timestamps that are T seconds (defult: 60 seconds) or less from the maximum timestamp that has been processed.

As new payments come in, edges that were formed between users with payments older than T seconds from the maximum timestamp are evicted. 


**Notes:** 
* Payments that are out of order and fall within the T second window of the maximum timestamp processed, or in other words, are less than T seconds from the maximum timestamp being processed, will create new edges in the graph. However, payments that are out of order in time and outside the T-second window (or more than T seconds from the maximum timestamp being processed) are ignored. Such payments won't contribute to building the graph. 

* The transactions that are missing data (e.g. missing an 'actor' field) are ignored by the code and would not affect the graph. 


**Classes and Data Structures**

The code includes three classes namely: Graph, Vertex, and DataStorage.

The Graph class works based on "Adjacency List" approach.

The DataStructure class stores the information of the edges of the graph in a dictionary. The timestamps of the transactions are used as the key. The vertices of each edge create a tuple which is stored in a set under the corespounding dictionary key (i.e. timestamp). Therefore, the set of all the edges for a specific timestamp can be accessed in O(1). In addition, the operations on the set are add(), remove(), and pop() for which the performance is in O(1). 

As the stream of timestamps is provided to the code, new timestamps are placed in a priority queue using the heapq module. Furethermore, any transation that fall out of the T seconds window will be evicated. For these transactions, the timestamp are removed from the priority queue, and the correspunding of data and edges will be removed from the dataStructure and graph respectively.  











