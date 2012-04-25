package database;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;


public class DataManager {

	 public static Map<String, DataFile> dataFiles = new HashMap<String, DataFile>();

	// Create File
 	public static DataFile createFile(String fileName, Map<String, Integer> descriptor) {
		
		if(dataFiles.containsKey(fileName))
			throw new IllegalArgumentException("fileName");
		DataFile f = new DataFile(fileName,descriptor);
		dataFiles.put(fileName, f);
		return f;
		
	}
	
	// Restore File 
	public static DataFile restoreFile(String fileName){
		if(dataFiles.containsKey(fileName))
			throw new IllegalArgumentException("fileName");
		
		File f = new File(fileName+".file");
		if(!f.exists()){
			throw new IllegalArgumentException("fileName");
		}
		
		DataFile f1 = null;
		try {
			FileInputStream fis = new FileInputStream(fileName+".file");
			ObjectInputStream in = new ObjectInputStream(fis);
			f1 = (DataFile) in.readObject();
			in.close();
		} catch (IOException ex) {
			ex.printStackTrace();
		}catch (ClassNotFoundException ex){
			ex.printStackTrace();
		}
		
		// Update the dataFiles map 
		dataFiles.put(fileName, f1);
		return f1;
	}

	// On exit
	public static void exit(){
		
	    if(dataFiles != null) {
	    	
			  for (Entry<String, DataFile> df : dataFiles.entrySet())
	  		  {
				  DataFile d = df.getValue();
				  Map<String, Index> indexF = new HashMap<String, Index>();
				  indexF = d.indexFiles;
				  
				  for(Entry<String,Index>e : indexF.entrySet() )
				  {
		                 Index iObj = e.getValue();
		                 iObj.dumpIndex();
		                 iObj = null;					  
				  }
				 d.dumpFile();
	  		  }
		 dataFiles.clear();
	    }
	}
	
	//Print individual row 
     public static String print(Map<String, String> record){
		
		String result="";
        for (Entry<String, String> e : record.entrySet())
		  result+="\t"+e.getKey()+": "+e.getValue()+"\n"; 
		return result;
	}
}
