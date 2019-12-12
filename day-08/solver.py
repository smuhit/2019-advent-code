image_width = 25
image_height = 6

raw_data = open('input').read()
layers = []
for i in range(0, len(raw_data), image_width * image_height):
    layers.append([])
    for layer in [raw_data[i:i + image_width * image_height]]:
        for j in range (0, len(layer), image_width):
            layers[-1].append(layer[j:j + image_width])

# Part 1
fewest_0 = None
for idx, layer in enumerate(layers):
    if fewest_0 is None or sum((x.count('0') for x in layer)) < sum((x.count('0') for x in layers[fewest_0])):
        fewest_0 = idx

print('Number of 1s with 2s in the layer with fewest 0s is', sum((x.count('1') for x in layers[fewest_0])) * sum((x.count('2') for x in layers[fewest_0])))

# Part 2 -- answer will be printed to screen
character_to_print = {
    '0': ' ',
    '1': '█'
}
for height in range(image_height):
    for width in range(image_width):
        idx = 0
        while layers[idx][height][width] not in character_to_print:
            idx += 1
        print(character_to_print[layers[idx][height][width]], end='')
    print()
