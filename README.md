# Keycap Label Maker

# Usage
1. Create `.json` (qmk-like) configuration file (you can use `config.example.json` as a reference)
2. Install requirements with `pip install -r requirements.txt`
3. Run `python main.py <your_config>.json`
4. your labels are in the `output` directory. (individual labels and grid image for printing)

# TODO
 - add optional front area (https://deskthority.net/wiki/Relegendable_key)
 - add downloading icons from:
   - material design icons (mdi) - https://pictogrammers.com/library/mdi/
   - fontawesome (fa) - https://fontawesome.com/
   - custom-brand-icons (phu) - https://github.com/elax46/custom-brand-icons

# File structure
generated with [tree](https://gitlab.com/nfriend/tree-online)
```
.
├── requirements.txt
├── main.py
├── config.example.json
└── (others, unneeded)/
    ├── icons/
    │   ├── mdi/
    │   │   └── svg/png files
    │   ├── phu/
    │   │   └── svg/png files
    │   ├── fa/
    │   │   └── svg/png files
    │   └── (others)/
    │       └── svg/png files
    └── output/
        ├── keycap_{number}.png - individual labels
        └── grid.png - all labels on a grid for printing
```
