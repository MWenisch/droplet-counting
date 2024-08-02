from cv2 import imreadmulti
from tifffile import TiffFile
import re
from droplet_counting import *
from plotting import *

def run_droplet_count():
    ##### Following parameters need to be set #####
    # Add path of the parent folder. Include the experiment number in the following format expXXX
    directory = "<path/expXXX>"
    # Add filename of the image/stack.
    # The name should include the time when the video was started after the addition of EDC in the following fromat: XXminYYsec
    filename = "<filename-XXminYYsec.tif>"

    show_mask_plot = False # True --> shows the threshold and mask of each individual image

    ##If needed adjust the lower boundary for creating a mask. Keep it constant for experiments you want to compare
    lower_boundary_threshold = 15

    ##### Code is running with the given parameters #####
    # Extract experiment number from directory
    pattern_exp_num = r'exp(\d+)'
    match_exp_num = re.search(pattern_exp_num, directory)
    experiment_num = match_exp_num.group(1)

    #create parameter for naming the output file
    specified_name = experiment_num + '_thresh'+ str(lower_boundary_threshold)

    # Extract starting time from the file name
    pattern_time = r'(\d+)min(\d+)sec'
    match = re.search(pattern_time, filename)
    start_min = int(match.group(1))
    start_sec = int(match.group(2))
    # Calculate the Starting time in sec
    starting_t = start_min * 60 + start_sec

    # Generate the path of the video/image for passing on to the counting function
    path = directory + '/' + filename  # under windows use '\' instead of '/'

    # create output lists
    droplet_num = []
    droplet_rad = []
    droplet_area = []

    #Get metadata of the Tif file
    with TiffFile(path) as tif:
        assert tif.is_imagej
        tags = tif.pages[0].tags
        x_resolution = tags['XResolution'].value
        y_resolution = tags['YResolution'].value

        for page in tif.pages:
            for tag in page.tags:
                tag_name, tag_value = tag.name, tag.value

    frame_interval = tif.imagej_metadata['finterval']
    pixel_size = 1 / (x_resolution[0] / x_resolution[1])
    #print(' x-reolution is:', x_resolution,'\n','y-reolution is:',y_resolution,'\n', 'frame rate is:',frame_interval,'\n', 'pixel size:', pixel_size)

    #Calculate the minimal droplet size, all droplets below the size won't be counted
    minimal_droplet_size_in_pixel = 0.242 / pixel_size #0.242

    #Read Tif file with stack or image to count the droplets
    _, input = imreadmulti(path)
    for image in input:
        drop_nr, radius, drop_area = droplet_counting(image, lower_boundary_threshold,minimal_droplet_size_in_pixel, show_mask_plot)
        droplet_num.append(drop_nr)
        droplet_rad.append(radius)
        droplet_area.append(drop_area)
        output_file = directory + specified_name + '_droplet_count.csv'
    print("#image:", len(droplet_num), "count", drop_nr)

    #print(droplet_num)
    #Generate Output File with droplet number, radius and area
    with open(output_file, mode='w') as output:
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        slice_number = 1
        writer.writerow(['Slice number', 'Time [s]', 'Droplet number','Radius [μm]', 'Area [μm^2]' ])
        for number in droplet_num:
            time = starting_t + (slice_number-1)*frame_interval
            out_rad = ''
            out_area = ''
            for i in range(0,len(droplet_area[slice_number-1])):
                area = droplet_area[slice_number - 1][i]
                radius = droplet_rad[slice_number - 1][i]
                r_um = pixel_size * radius
                area_um = area * pixel_size * pixel_size
                out_rad += str(r_um) + '_'
                out_area += str(area_um) + '_'
            writer.writerow([slice_number,time, number, out_rad[:-1], out_area[:-1]])
            slice_number += 1

    #Plot the droplet number over time and save the plot in the directory
    plotting(output_file, directory, specified_name)

if __name__ == '__main__':
    run_droplet_count()