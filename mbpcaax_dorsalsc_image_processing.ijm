//set up directories
//input path is the folder where all the images to be processed are
input_path = " ";
output_path = " " + "Cropped_";
if (!File.exists(output_path)) {
	File.makeDirectory(output_path);
}
list = getFileList(input_path);
//iterate through images in input path
for ( i=0; i<list.length; i++ ) { 
	if (endsWith(list[i], ".czi")) {
		//open image, get rid of brightfield
		img = "open=["+input_path+list[i]+"] autoscale color_mode=Grayscale rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT";
		run("Bio-Formats Importer", img);
		//comment out bottom two for one channel image
		run("Split Channels");
		close();
		getDimensions(width, height, channels, slices, frames);
		
		//rotate image along spinal axis
		makeLine(265, 196, 994, 149);
		waitForUser("Adjust line to align with spinal cord tilt.");
		getLine(x1, y1, x2, y2, width);
	    angle = (180.0/PI)*atan2(y1-y2, x2-x1);
	    setSlice(1);
	    for (j = 1; j < slices; j++) {
			run("Arbitrarily...", "angle="+angle+" interpolate");
			run("Next Slice [>]");
	    }
		title = File.nameWithoutExtension;
		
		//set up directory for slices
		slice_path = output_path + "slices_" + title + "/";
		File.makeDirectory(slice_path);
		print(title);
		
		//set up ROIs
		// rectangle below is for spinning disk 10x
		makeRectangle(297, 247, 705, 45);
		//for 20x image use bottom rectangle
		//rectangle below for spinning disk 20x
		//makeRectangle(1122, 1848, 2802, 246);
		//rectangle below is 20x lsm980 1.3 zoom
		//makeRectangle(111 ,441, 3879 , 294);
		setSlice(round(slices/2));
		waitForUser("Center ROI on dorsal column (top of stack). This should be the first slice you want included.");
		Roi.getBounds(x,y,w,h);
		start_slice = getSliceNumber();
		print("Start slice set to: " + start_slice);
		waitForUser("Center ROI on dorsal column (bottom of stack). This should be the last slice you want included.");
		Roi.getBounds(x2,y2,w2,h2);
		end_slice = getSliceNumber();
		print("End slice set to: " + end_slice);
		
		//do maths to find slope
		n = end_slice - start_slice;
		ydif = y-y2;
		Stack.setSlice(start_slice)
		
		//iterative cropping along slope
		for (j = 0; j < n; j++) {
			makeRectangle(x, y-((ydif/n)*(j+1)), 705, 45);
			//below is for 20x
			//change values for different 20x
			//makeRectangle(x, y-((ydif/n)*(j+1)), 3879 , 294);
			run("Duplicate...", "title=slice00" + toString(j));
			slicetitle = getTitle();
			saveAs("Tiff", slice_path + slicetitle + ".tif");
			close();
			run("Next Slice [>]");
		}
		close("*");
	}
}
