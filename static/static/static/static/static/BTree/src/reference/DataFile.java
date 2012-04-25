package reference;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

public class DataFile implements Serializable {
	private static final long serialVersionUID = 4298564775253437099L;
	String fileName;
	Map<String, Integer> descriptor;
	public Map<Integer, Map<String, String>> records = new HashMap<Integer, Map<String, String>>();
	
	public Map<String, String> getRecord(int recordId) {
		return records.get(recordId);
	}
}