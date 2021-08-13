# from global_land_mask import globe
# # import numpy as np

# from lightarray import getLedCoords

# if __name__ == '__main__':
#   coords = getLedCoords()
#   # print(coords)

#   sourceFile = open('ledcoords_land.txt', 'w')

#   for i in coords:
#     pointlong1 = (i[1] + 180) % 360 - 180
#     land = globe.is_land(i[0],pointlong1)
#     print('lat={}, lon={} is on land: {}'.format(i[0],i[1],land))
    
#     print('{},{},{}'.format(i[0],i[1],land), file = sourceFile)

#   sourceFile.close()