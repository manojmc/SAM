package database;

import java.io.*;
import java.util.ArrayList;
import java.util.Collection;
import java.util.ConcurrentModificationException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.NoSuchElementException;
import java.util.TreeMap;

public class DataFile implements Serializable {
	private static final long serialVersionUID = 4298564775253437099L;
	String fileName;
	Map<String, Integer> descriptor;
	public Map<Integer, Map<String, String>> records;
	// my own variables 
	Map<String, Index> indexFiles;
	public Integer recordID;
	public Map<Integer,Integer> alive;
	Integer index_counter;
	ArrayList<Integer> current_list;
	// Constructor
	DataFile(String fname, Map<String, Integer> schema)
	{
		descriptor = schema;
		fileName = fname;
		records = new TreeMap<Integer, Map<String, String>>();
		recordID=-1;
		indexFiles = new HashMap<String, Index>();
		alive = new HashMap<Integer,Integer>();
		index_counter =0;
		//current_list = 
	}
	
	// CREATE INDEX and return INDEX object
	public Index createIndex(String indexName, String column)
	{	
		// Check if column's length is > 24
		if(descriptor.get(column) >24)
			throw new IllegalArgumentException("column");
		// Check if there is already an index with that name 
		if(indexFiles.containsKey(indexName))
			throw new IllegalArgumentException("indexName");
		// Create an index object and instantiate obj of node class 
		Index a = new Index(indexName,fileName,column,this);
		a.initiator.initialize();
		int d =0;
		for (Entry<Integer, Map<String, String>> e : records.entrySet())
			a.initiator.insertNode(e.getValue().get(column),e.getKey());
		
		indexFiles.put(indexName, a);
		return a;	
	}
	
	// Get the record given a recordID
	public Map<String, String> getRecord(int recordId) {
		
		if(!records.containsKey(recordID) || alive.get(recordID)==0)
			return null; 
		return records.get(recordId);
	}
	
	// INSERT record into file and return recordID
	public int insertRecord(Map<String, String> record)
	{	
		Collection<Integer> size = descriptor.values();
		Iterator<Integer> max = size.iterator();
		for(Entry<String, String> e: record.entrySet())
		{
           if(!descriptor.containsKey(e.getKey()))
		    	throw new IllegalArgumentException("Column Name");
			if(e.getValue().length() > max.next())
				throw new IllegalArgumentException("Length of value is greater!");
		}
		recordID++;
		// Insert Record into map
		alive.put(recordID,1);
		records.put(recordID, record);
		
		// Update the indexes
		for(Entry<String,Index>e: indexFiles.entrySet() )
		   e.getValue().initiator.insertNode(record.get(e.getValue().columnName), recordID);
		
		return recordID;	
	}
	
	
	//Dump File
	public void dumpFile()
	{
		ObjectOutputStream st = null;
		try {
			String fname = fileName + ".file";
			st = new ObjectOutputStream(new BufferedOutputStream(new FileOutputStream(fname)));
			st.writeObject(this);
			st.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	
	// View file prints the file contents in a particular format
	public String viewFile()
	{	
		String result="";
        for (Entry<Integer, Map<String, String>> e : records.entrySet())
        {
          if(alive.get(e.getKey())==0)
        	continue;
          result+= e.getKey() + ":\n"; 
  		  Map<String,String> row = e.getValue(); 
  		  for (Entry<String, String> eachColumn : row.entrySet())
  			  result+="\t"+eachColumn.getKey()+": "+eachColumn.getValue()+"\n";
  	    }
		return result;	
	}
	
	public void dropFile()
	{
		File fileObj = null;

		  for (Entry<String, Index> i : indexFiles.entrySet())
  		  {
  			  Index indexOfFile = i.getValue();
  			fileObj = new File(i.getKey());
			if(fileObj.exists()) {
				fileObj.delete();
			}
			indexFiles.remove(i.getKey());

  		  }
			records = null;
			descriptor = null;		
	}
	
	public Index restoreIndex(String indexName){
		
		if(indexFiles.get(indexName) != null) {
			throw new IllegalArgumentException("Index " + indexName +"already exists in memory");			
		}

		if(new File(fileName + indexName).exists() == false) {
			throw new IllegalArgumentException("No" +indexName + "on disk");
		}

		ObjectInputStream in = null;
		Index indexObj = null;

		try {
			in = new ObjectInputStream(new BufferedInputStream(
					new FileInputStream(fileName + indexName)));
			indexObj = (Index) in.readObject();
			in.close();

			}
		catch(Exception e){
		}

		// Update the indexFiles map
		indexFiles.put(indexName, indexObj);
		return indexObj;
	}

	public Iterator<Integer> iterator()
	{
		return new FileIterator();
		
	}
	
	private class FileIterator implements Iterator<Integer>
	{
		
		int cursor = -1;
		int lastret = -1;
		int modcount = -1;
		
		public void CheckForCoModificaton() {
			 if(modcount!=cursor) {
				 throw new ConcurrentModificationException();
			 }
		}
		
		@Override
		public boolean hasNext() {
			// TODO Auto-generated method stub
			int flag=0;
//			if(cursor==-1 && records.size()!=0)
//				return true;
			if(cursor < records.size()-1)
			{
				while(alive.get(cursor+1)==0) 
				{
					cursor++;
					modcount++;
					if(cursor == records.size()-1)
					{
					flag = 1;
					break;
					}
				}
				if(flag == 1)
					return false;
				return true;
			}
			else 
			  return false;
		}

		@Override
		public Integer next() {
			// TODO Auto-generated method stub
			//CheckForCoModificaton();
			try {
				  cursor += 1;
				  modcount++;
				  return cursor;
				  } catch (IndexOutOfBoundsException e) {
					  	throw new NoSuchElementException();
				     }
				  }
		

		@Override
		public void remove() {
			//CheckForCoModificaton();
			alive.put(cursor,0);
			//System.out.print(cursor+" ");
		}
	}
}
