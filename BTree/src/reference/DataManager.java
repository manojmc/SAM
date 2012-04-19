package reference;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;


public abstract class DataManager {

	static Map<String, DataFile> dataFiles = new HashMap<String, DataFile>();
	
	public static DataFile restoreFile(String fileName){
		if(dataFiles.containsKey(fileName))
			throw new IllegalArgumentException("fileName");
		
		File f = new File(fileName+".file");
		if(!f.exists()){
			throw new IllegalArgumentException("fileName");
		}
		DataFile dataFile = null;
		try {
			FileInputStream fis = new FileInputStream(fileName+".file");
			ObjectInputStream in = new ObjectInputStream(fis);
			dataFile = (DataFile) in.readObject();
			in.close();
			
			return dataFile;
			
		} catch (IOException ex) {
			ex.printStackTrace();
		}catch (ClassNotFoundException ex){
			ex.printStackTrace();
		}
		return null;
	}

	public static void exit(){
		dataFiles.clear();
	}
}
