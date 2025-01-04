import json

frame_length_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Information/valid_frames_length.json'
array_data = [
    "012b09a0", "1aa4e7f6", "2b84174e", "3c5e3be8", "505ed57c", "6a6547d7", "9069547d", "a42fcfa9", "b87840e1",
    "c7543b31", "d26036cd", "e7ef3b9d", "fb4a7958", "0299d8d6", "1b664206", "2bd72d60", "3d04522a", "5251dbb9",
    "6c88a53b", "90d7f538", "a5249886", "b8e00b22", "c7b07fea", "d33e1c97", "ebd1dbad", "fb57abac", "06eb2803",
    "1ef6cb7b", "2c22cd4e", "3d8b1ee0", "567bfc5a", "71d35513", "9323c19c", "a74b52eb", "b97c4e2b", "c89239d8",
    "d3ba30b3", "ec6fd219", "ff64095e", "0d0030a7", "1f17cd7c", "2ca20519", "4027a35b", "5834b092", "7223bf62",
    "95718597", "a87bbd47", "ba5644c3", "c9a2645e", "d41a62d4", "ed5ec3c5", "1123fd76", "2112a80d", "2cc7839e",
    "429d96d4", "6073aa21", "75a8cadb", "957c33a7", "aa8df541", "bd34e772", "c9dfbd0c", "d4f4cf55", "ed82ce50",
    "1220b722", "257cca89", "2d0f3000", "435d99e0", "6312935f", "768c5810", "95a50b7d", "aa925437", "c29ce49d",
    "ca440c64", "d501f685", "ef81cd52", "15e09c8c", "2a02f752", "2d802cb8", "44a4d836", "63263f3f", "7a8cfc91",
    "97f5bbc8", "aaa8bd16", "c34989e3", "caf53839", "d50fa72e", "f10e23dd", "15e281a9", "2a19d8a2", "30446667",
    "454c7bb5", "68d9fb6a", "7e52df6a", "9b318a9c", "ac8ecb27", "c4ecad66", "cfe04aff", "e0a22a9b", "f326bfb7",
    "1806a28d", "2ab06287", "3054dbaf", "48cd08af", "69398c01", "817263d6", "9ed568e9", "b643add8", "c4fd77f2",
    "cfff47c3", "e3d901dd", "f4b271d4", "19615388", "2b6e117d", "35dff164", "4d63d7df", "6976cf19", "86b8e4ec",
    "a10de0fc", "b692e3cb", "c587e43b", "d084134f", "e568ca41", "f6cdaca7", "1a4b95d3", "2b827e3a", "39f0d139",
    "4d6a99ec", "6a47103e", "8b935b9f", "a16e9661", "b7b9f632", "c705c014", "d0a07d68", "e78253f1", "f9bee2e2"
]

array_set = set(array_data)
with open(frame_length_path, 'r') as file:
    json_data = json.load(file)

missing_keys = {key: json_data[key] for key in json_data if key not in array_set}

print("JSON 中存在但数组中缺少的对象及其值:")
for key, value in missing_keys.items():
    print(f"{key}: {value}")
print("JSON 长度:", len(json_data))
print("数组长度:", len(array_data))


