import random_crack_api as rc

M = rc.RandomModel()
P = rc.Predictor()

data = [
    0.7798771050886941,   0.7764594926531374,  0.0775997725970583,
    0.8358194832175498,  0.19852184735623912,  0.7218955009670991,
   0.16042013608507366,   0.8288793889484478, 0.05896567656619234,
    0.8040386545403124,   0.5351933593904763,  0.7995846906681257,
     0.891940669109091,   0.4346996879608196,  0.3555296436497597,
    0.3526971852438816,   0.9726507634441235, 0.21127767331908398,
    0.4338956633478608, 0.007290404683589102,  0.6813121919514578,
    0.9622630919265656,   0.2820001915345105,  0.5184436118562614,
  0.005815363468923751,   0.9548070960078967,  0.4930666141058768,
    0.5574146531969204,   0.8365639628069714,  0.7698627251923043,
    0.8670358428693223,   0.7093135926227896,  0.2115395508096496,
    0.4062873030504184,   0.8596987138446179, 0.01416083784550537,
    0.9214051013485107,    0.749570529737992,  0.5673286641226083,
    0.6124657029671641,    0.708173837854881, 0.38248351608132514,
    0.6633576738844718,  0.13071118728398923,  0.7304487462851275,
    0.3986219156152062,   0.8090574834144479,  0.6539839573549349,
    0.7517814226477062,   0.5327770633082392,  0.5951893107537316,
    0.7160058801353062,   0.2965851300385616,  0.9947363147627879,
    0.9445851168602875,  0.06671954616434439,  0.5110567072700865,
    0.3623181353336564,  0.37363547165751676,  0.4062854551668942,
    0.9754023319531875,   0.5254242528241768,  0.3566062620292332,
    0.2137687110541524,   0.6300081967984208, 0.11953431805928383,
   0.47507056887773236,  0.20928422481734987,  0.3203082224099567,
   0.44791914093179175,  0.47803060394161223,   0.320170086452523,
    0.1581447142719259,  0.11806922019504418, 0.26044338425268876,
     0.561366656388073,   0.8630501115284215,  0.9569634980266908,
    0.7452325331047296,   0.9170348201858904, 0.45253385969439885,
    0.6127171543208587,  0.10561024585962309,  0.6028757232781898,
    0.5436856136268948,  0.18207708913427134,  0.7206379313893811,
    0.9077717654960311,  0.31500208412003117,  0.6917077348696139,
   0.31564744631405617,   0.5609788215983351,  0.8288166576516014,
    0.8054331045166949,   0.7884677442571162, 0.43490235914232467,
    0.9289473645693158,   0.3676708771478199, 0.07449252938655748,
    0.5237837783512014
]


print(len(data))

input_data = data[:68]
print(data[68])

M.input_samples(input_data, rc.InputType.RAW)

print(M.get_next(rc.InputType.RAW))