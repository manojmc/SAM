package database;

import java.io.BufferedOutputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.ConcurrentModificationException;
import java.util.Iterator;

import Implementation.Node;

public class Index implements Serializable{
	
   public Node initiator;
   String indexName="";
   String fileName="";
   String columnName="";
   DataFile parent;
   
//   ArrayList<Integer> myIndex = new ArrayList<Integer>();
   Index(String iname,String fname,String cname,DataFile parent1)
   {
	   initiator = new Node();
	    indexName= iname;
	    fileName=fname;
	    columnName=cname;
	    parent = parent1;
	    
   }

	public void dumpIndex() {
		ObjectOutputStream out = null;

		try {
			out = new ObjectOutputStream(new BufferedOutputStream(
					new FileOutputStream(fileName + indexName)));
			out.writeObject(this);
			out.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	
	public String viewIndex()
	{
		
		return initiator.callInorder(); 
	}
	
    
	public Iterator<Integer> iterator(String key)
	{
		IndexIterator a1 = new IndexIterator();
		ArrayList<Integer> temp = new ArrayList<Integer>(); 
		temp=initiator.callPIndex(key);
		   a1.myIndex = temp;
		   int ac =0;
//		   return a1;
//        for(int k = 0 ;k<temp.size();k++)
//        {
//        	Integer g = temp.get(k);
//        	if(parent.alive.get(g)==0)
//        	{
//        		a1.myIndex.remove(g);
//        		ac++;
//        	}
//        }
//        for(int y=0;y<temp.size();y++)
//			System.out.print(temp.get(y)+ " ");
//        System.out.println();
//        for(int y=0;y<a1.myIndex.size();y++)
//			System.out.print(a1.myIndex.get(y)+ " ");
//		System.out.println(key);
//        //System.out.println(temp.size()+" ======"+a1.myIndex.size());
//        	return new IndexIterator();
		return a1;
	}
	
	private class IndexIterator implements Iterator<Integer>{
		int cursor;
		ArrayList<Integer> myIndex;
		IndexIterator(){
			cursor = 0;
			myIndex=new ArrayList<Integer>();
			parent.index_counter=0;
			
		}

		@Override
		public boolean hasNext() {
			parent.index_counter = cursor;
			if(cursor!=parent.index_counter)
                 throw new ConcurrentModificationException();
			// TODO Auto-generated method stub
			if(cursor<myIndex.size())
			{
				while(parent.alive.get(myIndex.get(cursor))==0)
				{
				    if(cursor == myIndex.size()-1)
				    	return false;
					cursor++;
					parent.index_counter++;
				}
				return true;
			}
			else 
				return false;
			}

		@Override
		public Integer next() {
			
			if(cursor!=parent.index_counter)
                throw new ConcurrentModificationException();
			// TODO Auto-generated method stub
			Integer rid = myIndex.get(cursor);
			cursor++;
			parent.index_counter++;
			return rid;
		}

		@Override
		public void remove() {
			if(cursor!=parent.index_counter)
                throw new ConcurrentModificationException();
			Integer rid = myIndex.get(cursor-1);
            parent.alive.put(rid, 0);
           
		}

	}
	}
