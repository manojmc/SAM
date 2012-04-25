package Implementation;
import java.io.Serializable;
import java.util.ArrayList;

/*
 * This class will create a Node.The Node can be of two types
 * Type 1 : Internal Node
 * Type 2 : Leaf Node, If its a leaf Node it will directly point to data
 */

public class Node implements Serializable {

	/*
	 * Declaring for Leaf Node. If checkLeaf is true then the Node is a leaf Node.
	 * 
	 */
	public boolean isLeaf;
	public boolean alive;
	public Node parent ; //will be used for Leaf and Internal Node.
	public int fillRatio ; //will determine number of elements in the Node
	/*
	 * Internal Node Declarations
	 * 
	 */

	public ArrayList<String> index;
	public ArrayList<Node> nodePointer;
	public ArrayList<Integer> data;
	public Node root;
	public int max;
	public int min;
	public Node m;
	public Node right;
	public String indexPrint = "";
	public ArrayList<Integer> particularIndex;
	
	public int gc=0;
	public Node() {
		isLeaf = false;
		index = new ArrayList<String>();
		nodePointer = new ArrayList<Node>();
		data = new ArrayList<Integer>();
		parent = null;
		alive = true;
		right = null;
		
	}	
		
	public void initialize()
	{
		root = TreeIndexing.root;
		max = 4;
		min = 2;
		m = null;
	}
	
	//Inorder Traversal of the Nodes
	
	public String callInorder()
	{	
		//System.out.println("inside callInodree");
		String s = "\n\n"+inOrderTraversal(root,0);
		//System.out.println(s);
		return s;		
	}
    
    
	
	//View Particular entry in an Index starts	
	public ArrayList<Integer> callPIndex(String s)
	{	particularIndex = new ArrayList<Integer>();
		Node n = valuePIndex(root,s);
		
		for(int i=0;i<n.index.size();i++)
		{
			if(n.index.get(i).equals(s))
			{	
				for(int k=0;k<n.nodePointer.get(i).data.size();k++)
				particularIndex.add(n.nodePointer.get(i).data.get(k));
			break;
			}
		}
		
		return particularIndex;
	}	
	
	public Node valuePIndex(Node n,String s)
	{
		while(n.nodePointer.get(0).data.isEmpty())
		{int i=0;
			while(i< n.index.size() && n.index.get(i).compareTo(s)<0)
			{
				i++;				
			}
			
			if(i< n.index.size()&&n.index.get(i).compareTo(s)==0)
				i++;
			
			n = n.nodePointer.get(i);
		}
		return n;
	}
	//View Particular entry in an Index ends

	public String inOrderTraversal(Node n,int spaceIns)
    {
    		//traversing internal and root nodes
            for(int i=0;i<n.nodePointer.size();i++)
            {
                inOrderTraversal(n.nodePointer.get(i), spaceIns+1);
                if(i<n.index.size())
                {
                    for(int j=0;j<spaceIns;j++)
                    {                    
                    	indexPrint = indexPrint + ("\t");
                    }
                    String temp = n.index.get(i);
                    
                    if(n.equals(root)&& !n.nodePointer.get(i).data.isEmpty())
                    	indexPrint = indexPrint + temp+"\n"+"\t";
                    
                    if(n.nodePointer.get(i).data.isEmpty())
                    	indexPrint = indexPrint + temp+"\n";
                    else  
                    {	for(int k=0;k<n.nodePointer.get(i).data.size();k++)
                    	{indexPrint = indexPrint + temp+ " " + n.nodePointer.get(i).data.get(k) + "\n";
                    	if(k<n.nodePointer.get(i).data.size()-1)
                    	{
                    		for(int j=0;j<spaceIns;j++)
                    			indexPrint = indexPrint + ("\t");
                    	}
                    	}
                    }
                }
            }
             return indexPrint;

    }//inOrderTraversal
	
	
	//Inorder Traversal of the Nodes Ends
	
	public void insertNode(String key, Integer value)
	{
		Node leafNode = new Node();
		//changed
		leafNode.data.add(value);
		//changed
		leafNode.isLeaf = true;
		if(root != null)
		{
			  traverseNode(key, root);
		    insertLeaf(key, leafNode,m);
		}
		else
		{
			//System.out.println("No Root Created");
			root = new Node();
			root.index.add(key);
			root.nodePointer.add(leafNode);
			
		}
		
	}
	
	
	// To find the node where the leaf has to be inserted
	// Accepts the Key and root as paramenter and is called recursively
	// Returns the node 
	public int traverseNode(String key,Node n)
	{	
		int j = 0;
		while( j<n.index.size() && key.compareTo(n.index.get(j))==0)
		{
			j++;
		}
		
		if(j>0 && !n.nodePointer.get(0).isLeaf)
			traverseNode(key,n.nodePointer.get(j));
		
		if(n.nodePointer.get(0).isLeaf){
	     	m = n;
			return 1;
		}
		
		int i=0;
		while(i<n.index.size())
		{
			//System.out.println("traversal");
			// Traverse to left since key is smaller that first key in index node 
			if(key.compareTo(n.index.get(i))<0 ){
				traverseNode(key, n.nodePointer.get(i));
			   break;
			}
			// Traverse right
			else if ((i == n.index.size() -1) || (key.compareTo(n.index.get(i)) > 0 && key.compareTo(n.index.get(i+1)) < 0 )){
				traverseNode(key, n.nodePointer.get(i+1));
				break;
			}
			i++;
		}
		return 1; 
		
	}// Traversal
	
	// To insert the leafnode
	// If split occurs we call the modify index 
	public void insertLeaf(String key, Node toInsert,Node parentNode)
	{			boolean duplicate = false;
		        int pos = parentNode.index.size();
				for(int i=0;i<parentNode.index.size();i++)
				{
					if(key.compareTo(parentNode.index.get(i))<0)
					{
						pos = i;
						break;
					}
					else if(key.compareTo(parentNode.index.get(i))==0)
					{
						duplicate = true;
						pos = i;
						break;
					}
				}
				
				if(!duplicate)
				{
				parentNode.nodePointer.add(pos,toInsert);
				parentNode.index.add(pos,key);	
				}
				else
				{
					parentNode.nodePointer.get(pos).data.add(toInsert.data.get(0));
					duplicate = false;
				}
				 // If node is full 
				if(parentNode.index.size()>max)
				{
					 Node n = new Node();
					 //adding a right pointer to the newly created Node
					 Node tempRight = null;
					 tempRight = parentNode.right;
					 parentNode.right = n;
					 n.right = tempRight;
					 n.parent = parentNode.parent;
					 //adding right pointer ends
					 for(int i=0;i<=min;i++)
					 {
						 n.index.add(parentNode.index.get(min));
						 n.nodePointer.add(parentNode.nodePointer.get(min));
						 parentNode.index.remove(min);
						 parentNode.nodePointer.remove(min);
					 }
				     modifyIndex(n.index.get(0), parentNode, n);
				}
			
//			System.out.println();
//			for(int i=0;i<parentNode.index.size();i++)
//			{
//			System.out.print(parentNode.index.get(i));
//			}
//			System.out.println("-----");
			
	}
		
	// Modify index
	public void modifyIndex(String key,Node left, Node right)
	{
		// If split at root 
		if(left.parent==null)
		{
			//System.out.println("new root");
			Node n = new Node();
			n.index.add(key);
			n.nodePointer.add(left);
			n.nodePointer.add(right);
			root = n;
			left.parent =root;
			right.parent = root;
		}
		
		else 
		{
		 Node parentNode = left.parent;
		 int pos = parentNode.index.size();
			for(int i=0;i<parentNode.index.size();i++)
			{
				if(key.compareTo(parentNode.index.get(i))<0)
				{
					pos = i;
					break;
				}
			}
		 parentNode.index.add(pos,key);
		 parentNode.nodePointer.add(pos+1,right);
		 //System.out.println("########### "+ parentNode.nodePointer.get(pos+1).index.get(0));
		 // If node is full 
		 if(parentNode.index.size()>max)
			{
				 Node n = new Node();
				 // Get the split key 
				 String new_key = parentNode.index.get(min);
				 parentNode.index.remove(min);
				 // Move the half in parent node to new node 
				 for(int i=0;i<min;i++)
				 {
					 n.index.add(parentNode.index.get(min));
					 n.nodePointer.add(parentNode.nodePointer.get(min+1));
					 parentNode.index.remove(min);
					 parentNode.nodePointer.remove(min+1);
					 //made a change from parentNode to n and below
					 n.nodePointer.get(i).parent = n;
				 }
				 n.nodePointer.add(parentNode.nodePointer.get(min+1));
				 n.parent = parentNode.parent;
				 n.nodePointer.get(min).parent = n;
				 parentNode.nodePointer.remove(min+1);

				 // Call recursive function again 
				 modifyIndex(new_key,parentNode,n);
			}
		 
		}//elsel 	
		
	 }// rec fun
	

}
