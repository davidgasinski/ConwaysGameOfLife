import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json

# values for the grind
ON = 128
OFF = 0
vals = [ON,OFF]

def randomGrid(N):
    return np.random.choice(vals, N*N, p=[0.2,0.8]).reshape(N,N)

def addGlider(i, j, grid):
    glider = np.array([[0,0,128],
                    [128, 0,128],
                    [0,128,128]])
    grid[i:i+3, j:j+3] = glider

def addGosperGliderGun(i, j, grid):
    gun = np.zeros(11*38).reshape(11,38)

    gun[5][1] = gun[5][2] = 128
    gun[6][1] = gun[6][2] = 128

    gun[3][13] = gun[5][14] = 128
    gun[4][12] = gun[4][16] = 128
    gun[5][11] = gun[5][17] = 128
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 128
    gun[7][11] = gun[7][17] = 128 
    gun[8][12] = gun[8][16] = 128
    gun[9][13] = gun[9][14] = 128

    gun[1][25] = 128
    gun[2][23] = gun[2][25] = 128
    gun[3][21] = gun[3][22] = 128
    gun[4][21] = gun[4][22] = 128
    gun[5][21] = gun[5][22] = 128
    gun[6][23] = gun[5][25] = 128
    gun[7][25] = 128

    gun[3][35] = gun[3][36] = 128
    gun[4][35] = gun[4][36] = 128

    grid[i:i+11, j:j+38] = gun

def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + 
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/128)
            if grid[i,j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i,j] = OFF
            else:
                if total == 3:
                    newGrid[i,j] = ON
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def main():
    #open json and extract parameters
    with open('conway.json') as f:
        config = json.load(f)
    
    N = 100
    if (int(config['grid-size']) > 8):
        N = int(config['grid-size'])
    
    updateInterval = int(config['interval'])
    if (int(config['interval']) == 0):
        updateInterval = 50
    
    grid = np.array([])

    if (config['glider'].lower() == 'true'):
        grid = np.zeros(N*N).reshape(N,N)
        addGlider(1,1,grid)
    elif (config['gosper'].lower() == 'true'):
        grid = np.zeros(N*N).reshape(N,N)
        addGosperGliderGun(10,10,grid)
    else: 
        #random grid
        grid = randomGrid(N)
    
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig,update, fargs=(img, grid, N, ),
                                  frames = 10,
                                  interval = updateInterval,
                                  save_count= 50)
    plt.show()

if __name__ == '__main__':
    main()

                                
    


    
            
