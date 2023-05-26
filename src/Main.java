import java.io.*;
import parcs.*;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.util.Arrays;

public class Main implements AM 
{
    public static void main(String[] args) {
        task curtask = new task();
        curtask.addJarFile("Main.jar");
        (new Main()).run(new AMInfo(curtask, (channel)null));
        curtask.end();
    }

    public void run(AMInfo info) {
		BufferedImage originalImage = null;
		try {
			originalImage = ImageIO.read(new File("Input.jpg"));
		} catch (IOException e1) {
			e1.printStackTrace();
		}
		
		long startTime = System.nanoTime();
		
		int w = originalImage.getWidth();
		int h = originalImage.getHeight();
		System.out.println("Image width:\t" + w);
		System.out.println("Image height:\t" + h);
		BufferedImage kmeansImage = new BufferedImage(w, h, originalImage.getType());
		Graphics2D g = kmeansImage.createGraphics();
		g.drawImage(originalImage, 0, 0, w, h, null);
		
		int[] rgb = new int[w * h];
		int count = 0;
		for (int i = 0; i < w; i++) {
			for (int j = 0; j < h; j++) {
				rgb[count++] = kmeansImage.getRGB(i, j);
			}
		}
		
		int[] rgb1 = Arrays.copyOfRange(rgb, 0, rgb.length/2);
		int[] rgb2 = Arrays.copyOfRange(rgb, rgb.length/2, rgb.length);

        point p1 = info.createPoint();
        channel c1 = p1.createChannel();
        p1.execute("KMeans");
        c1.write(rgb1);
        
        point p2 = info.createPoint();
        channel c2 = p2.createChannel();
        p2.execute("KMeans");
        c2.write(rgb2);
        
        System.out.println("Waiting for result...");
        int[] k_values1 = (int[]) c1.readObject();
        int[] k_values2 = (int[]) c2.readObject();
        int[] k_values = new int[k_values1.length + k_values2.length];
        
        System.arraycopy(k_values1, 0, k_values, 0, k_values1.length);  
        System.arraycopy(k_values2, 0, k_values, k_values1.length, k_values2.length);
        
        for (int i = 0; i < rgb.length; i++) {
			double min_dist = Double.MAX_VALUE;
			int cluster_index = 0;
			for (int j = 0; j < k_values.length; j++) {
				int a_dist = (getAlpha(rgb[i]) - getAlpha(k_values[j]));
				int r_dist = (getRed(rgb[i]) - getRed(k_values[j]));
				int g_dist = (getGreen(rgb[i]) - getGreen(k_values[j]));
				int b_dist = (getBlue(rgb[i]) - getBlue(k_values[j]));
				double dist = Math.sqrt(a_dist * a_dist + r_dist * r_dist + g_dist * g_dist + b_dist * b_dist);
				if (dist < min_dist) {
					min_dist = dist;
					cluster_index = j;
				}
			}
			
			rgb[i] = k_values[cluster_index];
        }
	
	    System.out.println("Result found.");
	    
	    count = 0;
	    for (int i = 0; i < w; i++) {
			for (int j = 0; j < h; j++) {
				kmeansImage.setRGB(i, j, rgb[count++]);
			}
		}
	    
	    long endTime = System.nanoTime();

		System.out.println("Time: " + (endTime - startTime)/1000000 + " milliseconds");

	    try{
	  	  ImageIO.write(kmeansImage, "jpg", new File("Res.jpg"));
	    } catch (IOException e) {e.printStackTrace(); return;}
    }
    
	public static int getRed(int pix) {return (pix >> 16) & 0xFF;}
	
	public static int getGreen(int pix) {return (pix >> 8) & 0xFF;}
	
	public static int getBlue(int pix) {return pix & 0xFF;}
	
	public static int getAlpha(int pix) {return (pix >> 24) & 0xFF;}
}
