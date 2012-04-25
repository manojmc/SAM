package Implementation;


import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectOutput;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import database.DataFile;
import database.DataManager;
import database.Index;



public class TreeIndexing {
	
public static Node root = null;	

	public static void main(String args[])
	{
//		Node n = new Node();
//		n.initialize();
		DataManager m1 = new DataManager();
		
		HashMap<String, Integer> m = new HashMap<String, Integer>();
		m.put("xyz", 20);
		DataFile f1 = m1.createFile("file1", m);
			try {
						FileInputStream fi = new FileInputStream("//Users//magizharasuthirunavukkarasu//Documents//workspace1//BTree//src//abc.txt");
						DataInputStream di = new DataInputStream(fi);
						BufferedReader br = new BufferedReader(new InputStreamReader(di));
						String readOneLine;
						while((readOneLine = br.readLine())!=null)
						{	
							//Reading line by line data from the file and putting it into Object of Student type
							String []StDetail = readOneLine.split(",");
							HashMap<String,String> eachRow = new HashMap<String,String>();
							for(int i=0;i<StDetail.length;i++)
							{	int j = i+1;
								eachRow.put("xyz", StDetail[i]);
							}
							f1.insertRecord(eachRow);
							//System.out.println(readOneLine);
						}
				
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
    		 Index x = f1.createIndex("first", "xyz");
             System.out.println(x.viewIndex());
             Iterator<Integer> i = f1.iterator();
             int k=0;
             while(i.hasNext() && k<10)
             {
            	 i.next();
            	 i.remove();
            	 k++;
             }
             Iterator<Integer> i2 = x.iterator("R");
             while(i2.hasNext())
             {
            	 System.out.println(i2.next());
            	 //i.remove();
             }
        
		
	}
	
	
}
