import math, random, sys, os, time
from PIL import Image

def gaussianRand():
    rand = 0;
    for i in range(0,6):
        rand += random.random();
    return rand/6;

def unitVector(v1):
    magnitude = math.sqrt(math.pow(v1[0],2) + math.pow(v1[1],2) + math.pow(v1[2],2));
    return [v1[0]/magnitude, v1[1]/magnitude, v1[2]/magnitude];

def addVector(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]];

def subtractVector(v1, v2):
    return [v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]];

def crossProduct(v1, v2):
    return [v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0]];

def dotProduct(v1, v2):
    return (v1[0]*v2[0]) + (v1[1]*v2[1]);

def getNormal(v1, v2, v3):
    vectorA = subtractVector(v2, v1);
    vectorB = subtractVector(v3, v1);
    return unitVector(crossProduct(vectorA, vectorB));

def displayLoading(count, finish, message):
    print(message + ": " + str(count) + "/" + str(finish));

def diamondSquareHeightmap(n, maxHeight, jitter, jitterFactor):
    size = int(math.pow(2,n)+1);
    heightmap = [];
    for i in range(0,size):
        heightmap.append([0]*size);
    
    heightmap[0][0] = random.random()*maxHeight;
    heightmap[0][size-1] = random.random()*maxHeight;
    heightmap[size-1][0] = random.random()*maxHeight;
    heightmap[size-1][size-1] = random.random()*maxHeight;

    for i in range(0,n):
        stride = int((size-1)/math.pow(2,i+1));
        radius = int((size-1)/math.pow(2,i));
        for j in range(0,int(math.pow(2,i))):
            for k in range(0,int(math.pow(2,i))):
                heightmap[stride + (radius*j)][stride + (radius*k)] = ((heightmap[(radius*j)][(radius*k)] + \
                                                                       heightmap[(stride*2) + (radius*j)][(radius*k)] + \
                                                                       heightmap[(radius*j)][(stride*2) + (radius*k)] + \
                                                                       heightmap[(stride*2) + (radius*j)][(stride*2) + (radius*k)])/4) + ((random.random()-0.5)*jitter);
        for j in range(0,int(math.pow(2,i+1)+1)):
            for k in range(0,int(math.pow(2,i)+(j%2))):
                averageCounter = 0;
                if(j == 0):
                    height1 = 0;
                else: 
                    height1 = heightmap[stride*(j-1)][stride*((j+1)%2) + (radius*k)];
                    averageCounter+=1;
                if(k == 0 and j%2 == 1):
                    height4 = 0;
                else:
                    height4 = heightmap[stride*j][stride*(((j+1)%2)-1) + (radius*k)];
                    averageCounter+=1;

                if(j == int(math.pow(2,i+1)+1) - 1):
                    height3 = 0;
                else:
                    height3 = heightmap[stride*(j+1)][stride*((j+1)%2) + (radius*k)];
                    averageCounter+=1;

                if(k == int(math.pow(2,i)+(j%2))-1 and j%2 == 1):
                    height2 = 0;
                else:
                    height2 = heightmap[stride*j][stride*(((j+1)%2)+1) + (radius*k)];
                    averageCounter+=1;
                heightmap[stride*j][stride*((j+1)%2) + (radius*k)] = ((height1+height2+height3+height4)/averageCounter) + ((random.random()-0.5)*jitter);
        jitter /= jitterFactor;
    lowestPoint = 10000;
    for i in range(0,size):
        for j in range(0,size):
            if(lowestPoint > heightmap[i][j]):
                lowestPoint = heightmap[i][j];
    highestPoint = -10000;
    for i in range(0,size):
        for j in range(0,size):
            if(highestPoint < heightmap[i][j]):
                highestPoint = heightmap[i][j];
            
    if(n>1):
        for i in range(0,size):
            heightmap[0][i] = lowestPoint;
            heightmap[1][i] = lowestPoint + (heightmap[1][i] - lowestPoint)*0.25;
            heightmap[2][i] = lowestPoint + (heightmap[2][i] - lowestPoint)*0.5;
            heightmap[3][i] = lowestPoint + (heightmap[3][i] - lowestPoint)*0.75;
            heightmap[size-1][i] = lowestPoint;
            heightmap[size-2][i] = lowestPoint + (heightmap[size-2][i] - lowestPoint)*0.25;
            heightmap[size-3][i] = lowestPoint + (heightmap[size-3][i] - lowestPoint)*0.5;
            heightmap[size-4][i] = lowestPoint + (heightmap[size-4][i] - lowestPoint)*0.75;
            
            heightmap[i][0] = lowestPoint;
            heightmap[i][1] = lowestPoint + (heightmap[i][1] - lowestPoint)*0.25;
            heightmap[i][2] = lowestPoint + (heightmap[i][2] - lowestPoint)*0.5;
            heightmap[i][3] = lowestPoint + (heightmap[i][3] - lowestPoint)*0.75;
            heightmap[i][size-1] = lowestPoint;
            heightmap[i][size-2] = lowestPoint + (heightmap[i][size-2] - lowestPoint)*0.25;
            heightmap[i][size-3] = lowestPoint + (heightmap[i][size-3] - lowestPoint)*0.5;
            heightmap[i][size-4] = lowestPoint + (heightmap[i][size-4] - lowestPoint)*0.75;
    
    img = Image.new('RGB', (len(heightmap[0]),len(heightmap[0])), "black");
    pixels = img.load();
    
    for i in range(len(heightmap[0])):
        for j in range(len(heightmap[0])):
            if(heightmap[i][j] - lowestPoint > (highestPoint - lowestPoint)/2):
                pixels[i,j] = (0,int(255*( ((heightmap[i][j]-lowestPoint) - ((highestPoint-lowestPoint)/2))/((highestPoint - lowestPoint)/2) )),0);
            else:
                pixels[i,j] = (10,10,200);
    img.save("map.bmp");

    return heightmap;

def createHexagonalTerrain(segment, scale, tile, maxHeightLimit, minHeightLimit, heightmap, smooth = True, quiet = True, outputRate = 1):
    vertices = [];
    verticesOBJ = [];
    texturesOBJ = [];
    normalsOBJ = [];
    facesOBJ = [];
    maxHeight = maxHeightLimit;
    
    preventOutput = False;

    if(tile):
        texturesOBJ.append([0,0]);
        texturesOBJ.append([0,1]);
        texturesOBJ.append([1,0]);
        texturesOBJ.append([1,1]);
    
    for i in range(0, segment):
        if(i==segment-1):
            tempVerticesOBJ = [];
        for j in range(0, segment):
            if(not smooth):
                facesOBJ.append(str((i*(segment+1)) + j + 1) + '/' + str(1) + '/' + str((((i*segment) + j)*2) + 1) + ' ' +\
                                str((i*(segment+1)) + j + 2) + '/' + str(2) + '/' + str((((i*segment) + j)*2) + 1) + ' ' +\
                                str(((i+1)*(segment+1)) + j + 1) + '/' + str(3) + '/' + str((((i*segment) + j)*2) + 1) );
                facesOBJ.append(str(((i+1)*(segment+1)) + j + 1) + '/' + str(3) + '/' + str((((i*segment) + j)*2) + 2) + ' ' +\
                                str((i*(segment+1)) + j + 2) + '/' + str(2) + '/' + str((((i*segment) + j)*2) + 2) + ' ' +\
                                str(((i+1)*(segment+1)) + j + 2) + '/' + str(4) + '/' + str((((i*segment) + j)*2) + 2) );

            else:
                facesOBJ.append(str((i*(segment+1)) + j + 1) + '/' + str(1) + '/' + str((i*(segment+1)) + j + 1) + ' ' +\
                                str((i*(segment+1)) + j + 2) + '/' + str(2) + '/' + str((i*(segment+1)) + j + 2) + ' ' +\
                                str(((i+1)*(segment+1)) + j + 1) + '/' + str(3) + '/' + str(((i+1)*(segment+1)) + j + 1) );
                facesOBJ.append(str(((i+1)*(segment+1)) + j + 1) + '/' + str(3) + '/' + str(((i+1)*(segment+1)) + j + 1) + ' ' +\
                                str((i*(segment+1)) + j + 2) + '/' + str(2) + '/' + str((i*(segment+1)) + j + 2) + ' ' +\
                                str(((i+1)*(segment+1)) + j + 2) + '/' + str(4) + '/' + str(((i+1)*(segment+1)) + j + 2) );
            #T1
            verticesOBJ.append([(-scale/2) + i*(scale/segment), heightmap[i][j], (-scale/2) + (j)*(scale/segment)]);
            if(j==segment-1):
                verticesOBJ.append([(-scale/2) + i*(scale/segment), heightmap[i][j+1], (-scale/2) + (j+1)*(scale/segment)]);
            if(i==segment-1):
                tempVerticesOBJ.append([(-scale/2) + (i+1)*(scale/segment), heightmap[i+1][j], (-scale/2) + (j)*(scale/segment)]);
                if(j==segment-1):
                    tempVerticesOBJ.append([(-scale/2) + (i+1)*(scale/segment), heightmap[i+1][j+1], (-scale/2) + (j+1)*(scale/segment)]);

            vertices.append([(-scale/2) + i*(scale/segment), heightmap[i][j], (-scale/2) + (j)*(scale/segment)]);
            vertices.append([(-scale/2) + i*(scale/segment), heightmap[i][j+1], (-scale/2) + (j+1)*(scale/segment)]);
            vertices.append([(-scale/2) + (i+1)*(scale/segment), heightmap[i+1][j], (-scale/2) + (j)*(scale/segment)]);
#            else:
#                textures.append([i/segment, j/segment]);
#                textures.append([i/segment, (j+1)/segment]);
#                textures.append([(i+1)/segment, j/segment]);
#		    
            vertsLength = len(vertices);
            triNormal = getNormal(vertices[vertsLength-3], vertices[vertsLength-2], vertices[vertsLength-1]);
            normalsOBJ.append(triNormal);
		    
            #T2
            vertices.append([(-scale/2) + (i+1)*(scale/segment), heightmap[i+1][j], (-scale/2) + (j)*(scale/segment)]);
            vertices.append([(-scale/2) + i*(scale/segment), heightmap[i][j+1], (-scale/2) + (j+1)*(scale/segment)]);
            vertices.append([(-scale/2) + (i+1)*(scale/segment), heightmap[i+1][j+1], (-scale/2) + (j+1)*(scale/segment)]);

#            else:
#                textures.append([(i+1)/segment, j/segment]);
#                textures.append([i/segment, (j+1)/segment]);
#                textures.append([(i+1)/segment, (j+1)/segment]);

            vertsLength = len(vertices);
            triNormal = getNormal(vertices[vertsLength-3], vertices[vertsLength-2], vertices[vertsLength-1]);
            normalsOBJ.append(triNormal);
            
            if(not quiet):
                if((time.time() % outputRate) < 0.05 and not preventOutput):
                    displayLoading(i*segment + j, segment*segment, "TER | Segm");
                    preventOutput = True;
                elif(time.time() % outputRate > 0.05):
                    preventOutput = False;

    normalsSmooth = [];
    for i in range(0, segment):
        tempNormalsSmooth = [];
        for j in range(0, segment):
            if(j > 0):
                norm0 = list(normalsOBJ[(((i*segment) + (j-1))*2)]);
                norm1 = list(normalsOBJ[(((i*segment) + (j-1))*2) + 1]);
            else:
                norm0 = [0,0,0];
                norm1 = [0,0,0];
            
            norm2 = list(normalsOBJ[(((i*segment) + j)*2)]);

            if(i > 0 and j > 0):
                norm3 = list(normalsOBJ[((((i-1)*segment) + (j-1))*2) + 1]);
            else:
                norm3 = [0,0,0];
            if(i > 0):
                norm4 = list(normalsOBJ[((((i-1)*segment) + j)*2)]);
                norm5 = list(normalsOBJ[((((i-1)*segment) + j)*2) + 1]);
            else:
                norm4 = [0,0,0];
                norm5 = [0,0,0];
            
            normalsSmooth.append( unitVector(addVector(norm0, addVector(norm1, addVector(norm2, addVector(norm3, addVector(norm4, norm5)))))) );
            if(j == segment-1):
                norm0 = list(normalsOBJ[(((i*segment) + (j-1))*2)]);
                norm1 = list(normalsOBJ[(((i*segment) + (j-1))*2) + 1]);
                if(i > 0):
                    norm2 = list(normalsOBJ[((((i-1)*segment) + (j-1))*2) + 1]);
                else:
                    norm2 = [0,0,0];
                normalsSmooth.append( unitVector(addVector(norm0, addVector(norm1,norm2))) );
            if(i == segment-1):
                if(j > 0):
                    norm0 = list(normalsOBJ[((((i-1)*segment) + (j-1))*2) + 1]);
                else:
                    norm0 = [0,0,0];
                norm1 = list(normalsOBJ[((((i-1)*segment) + j)*2)]);
                norm2 = list(normalsOBJ[((((i-1)*segment) + j)*2) + 1]);
                tempNormalsSmooth.append( unitVector(addVector(norm0, addVector(norm1,norm2))) );
                if(j == segment-1):
                    norm0 = list(normalsOBJ[((((i-1)*segment) + (j-1))*2) + 1]);
                    tempNormalsSmooth.append(norm0);
    
    normalsSmooth+=tempNormalsSmooth;
            


    verticesOBJ+=tempVerticesOBJ;
    if(smooth):
        return [verticesOBJ, texturesOBJ, normalsSmooth, facesOBJ];
    else:
        return [verticesOBJ, texturesOBJ, normalsOBJ, facesOBJ];

def createOBJ(vertices, textures, normals, faces, outputRate = 1):
    preventOutput = False;

    objString = "";
    for i in vertices:
        objString += "v " + str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n";
    for i in textures:
        objString += "vt " + str(i[0]) + " " + str(i[1]) + "\n";
    for i in normals:
        objString += "vn " + str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n";
    for i in faces:
        objString += "f " + i + "\n";
    return objString;
                
                
segments = 10;
scale = 600;
tile = True;
maxHeight = 75;
minHeight = 0;
quiet = True;
outputRate = 1;
jitter = 40;
jitterFactor = 1.5;
smooth = True;

for i in range(0, len(sys.argv)):
    if(sys.argv[i] == '-s' or sys.argv[i] == '--segment'):
        segments = int(sys.argv[i+1]);
    if(sys.argv[i] == '-z' or sys.argv[i] == '--scale'):
        scale = float(sys.argv[i+1]);
    if(sys.argv[i] == '-m' or sys.argv[i] == '--min'):
        minHeight = float(sys.argv[i+1]);
    if(sys.argv[i] == '-x' or sys.argv[i] == '--max'):
        maxHeight = float(sys.argv[i+1]);
    if(sys.argv[i] == '-v' or sys.argv[i] == '--verbose'):
        quiet = False;
    if(sys.argv[i] == '-r' or sys.argv[i] == '--rate'):
        outputRate = float(sys.argv[i+1]);
    if(sys.argv[i] == '-j' or sys.argv[i] == '--jitter'):
        jitter = float(sys.argv[i+1]);
    if(sys.argv[i] == '-f' or sys.argv[i] == '--factor'):
        jitterFactor = float(sys.argv[i+1]);
    if(sys.argv[i] == '-e' or sys.argv[i] == '--edges'):
        smooth = False;

print("Generating terrain");
timeStart = time.time();

heightmap = diamondSquareHeightmap(segments, maxHeight, jitter, jitterFactor);
terrain = createHexagonalTerrain(int(math.pow(2,segments)), scale, tile, maxHeight, minHeight, heightmap, smooth, quiet, outputRate);
OBJ = createOBJ(terrain[0], terrain[1], terrain[2], terrain[3], outputRate);

timeEnd = time.time();
print("Terrain generated in " + str("%.2f" % round(timeEnd - timeStart,2)) + "s");


file = open("terrain.obj", "w+");
file.write(OBJ);
file.close();
