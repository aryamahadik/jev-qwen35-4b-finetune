"""Pinned Taskmaster files (google-research-datasets/Taskmaster @ d92cb6af) and their sha256, shared by the TM builders."""
import _ibs_common as C

COMMIT = "d92cb6af3005f1dc09c39e75e7daf4a04905e00b"
BASE = f"https://raw.githubusercontent.com/google-research-datasets/Taskmaster/{COMMIT}/"
CACHE = C.CACHE / "taskmaster"
SHA = {
    "TM-1-2019/self-dialogs.json": "1e590ed0ccee279e40c2fb9e083d3b9417477c6bfe35ce5b2277167698dd858d",
    "TM-1-2019/woz-dialogs.json": "cd3bc4e968487315d412c044d30af2bf0a4b33c3ef8b74c589f1e1fa832bf72f",
    "TM-1-2019/train-dev-test/train.csv": "88e48f53524ed123dfc57733ccc23f80e176d1e057d7ea46a62a01ddce02626e",
    "TM-1-2019/ontology.json": "b8103a812799a8c0095800ba9fbf2b4654bccf7f099daa8a4a145c340a69bc52",
    "TM-1-2019/README.md": "05e1bc05724716ca7905f567a2ec30d99c8d2f5f58e926c2ca7d9da116002446",
    "TM-2-2020/README.md": "0e707d4cc31869e0c0337979f72ecef61fc4fcab2bfe3a4ec1a546b84bc17463",
    "TM-2-2020/data/flights.json": "86b37b5ae25f530fd18ced78800d30c3b54f7b34bb208ecb51842718f04e760b",
    "TM-2-2020/data/food-ordering.json": "0a042e566a816a5d0abebe6f7e8cfd6abaa89729ffc42f433d327df7342b12f8",
    "TM-2-2020/data/hotels.json": "975b0242f1e37ea1ab94ccedd7e0d6ee5831599d5df1f16143e71110d6c6006a",
    "TM-2-2020/data/movies.json": "6f67c9a1f04abc111186e5bcfbe3050be01d0737fd6422901402715bc1f3dd0d",
    "TM-2-2020/data/music.json": "e5db60d6576fa010bef87a70a8b371d293d48cde8524c1d3ed7c3022f079d95d",
    "TM-2-2020/data/restaurant-search.json": "fb9735f89e7ebc7c877f976da4c30391af6a6277991b597c0755564657ff8f47",
    "TM-2-2020/data/sports.json": "8191531bfa5a8426b1508c396ab9886a19c7c620b443c436ec10d8d4708d0eac",
    "TM-2-2020/ontology/flights.json": "1ebc5c982339d24b2dcf50677883fed65b7fcb95f01edbbd3be6357090893c33",
    "TM-2-2020/ontology/food-ordering.json": "79c1189c16f0ab937bad558c70a0b9b99358f9ed91ea65ce4af37c4b7d999063",
    "TM-2-2020/ontology/hotels.json": "22ae51ba546ee7ca03143097782817c4cdd0de74ac84893eaf40b8254aa866d3",
    "TM-2-2020/ontology/movies.json": "8403283526bb314e871850b98bb86a7987ef0af6fbbe4fb5a089ee9498584476",
    "TM-2-2020/ontology/music.json": "4bcd6dcf1cdc6bdb717e5fdc08b3472dc3d1f4da8a0f8aee917494d79a7fe338",
    "TM-2-2020/ontology/restaurant-search.json": "c9ead7985695b3feba1fb955e8407d806e4095f5459485adc5448ae89989e609",
    "TM-2-2020/ontology/sports.json": "52f9bbb86ebd9e2b3916185ad4e3e9b8b77d2164d96bd3b98ad67cbaa653757d",
    "TM-3-2020/README.md": "e80b5ecc4011ef75eea94be5c3beba927e54673db25fd60fc2ca8d5a413ca928",
    "TM-3-2020/data/data_00.json": "4edf97557e1aa7f654bf97994b5eae42653ef6d4f5e50136f7664d7e5cdff7b6",
    "TM-3-2020/data/data_01.json": "a4fef75ec7824bb3fb29b8afe9ed63f3354b81077bb9b6f58f2349bb60d660fc",
    "TM-3-2020/data/data_02.json": "25cb4788c4c857740152612397b0e687dfeade14c7dbfeed501a53290725aedf",
    "TM-3-2020/data/data_03.json": "5e1f15544f259c804438458f34a6c7f00400e30dba7648c37a0b31886c5dd903",
    "TM-3-2020/data/data_04.json": "17d8deb3bc6c3551c564cb9003a47202a835e011477b1e3c81711b083bf4064b",
    "TM-3-2020/data/data_05.json": "12e58018be7b42aa16968ab914d03c56af9fae9fb5feec7448e01f738c50d2fe",
    "TM-3-2020/data/data_06.json": "a4e290dafc6362ca8d4d786d6e70f6339297b0414cca4fe0ec79c1d383d65673",
    "TM-3-2020/data/data_07.json": "becec1c0e9b88781fbb81f5d032826f85d77756cfae7c37acbca9b4b2a470fdb",
    "TM-3-2020/data/data_08.json": "c2718197cedfb1ff7b830492ddbdc36c213ac98c83ba974ff0ea0eeeffdfe9b5",
    "TM-3-2020/data/data_09.json": "a8867eb49010fa735b3c0b2f47df4cc225c79b6ca919009db857f454cccc986d",
    "TM-3-2020/data/data_10.json": "88a8ce81f2c843c7a52a1a6c016d790e6547d5a3ffdd000ca00f0676c02e077b",
    "TM-3-2020/data/data_11.json": "10e5d2dadb7a55b08d41605498b46320fa2df7b87c71a820df4245e9eeeba4d1",
    "TM-3-2020/data/data_12.json": "be255d29439d10fc33bb222a1294da0af7ed4bdf8ede84c389d9b744e9cdf343",
    "TM-3-2020/data/data_13.json": "a477d4668398b86bc7f68f86c20a423e81b4dbc41002a5d605dee0c6cee250b8",
    "TM-3-2020/data/data_14.json": "92c7a0ca1fce8845610a7fdb00972750228351b2c2065e76120c328c806cc1e5",
    "TM-3-2020/data/data_15.json": "e67e9d649d29f3edc12796cb4b1308cc7cb89f676c12e96d8fea558510b6ee18",
    "TM-3-2020/data/data_16.json": "f0d3f22ee8b9224ea4efc57182f1620f849f3b90050cc04992319aab04e7b453",
    "TM-3-2020/data/data_17.json": "15c469a030aae16a98969675b238f368436ec0a5074f3eb79458fdc81cf489d4",
    "TM-3-2020/data/data_18.json": "28dfe3f65c1cd7bab8ed9da0e667ee1aec1561cf41237531f30c889cafb0997d",
    "TM-3-2020/data/data_19.json": "7ae99d1237c25519269c3e6969ab0ecd88509828c436cbecb8a86831007c3868",
    "TM-3-2020/splits/train/train-aa.tsv": "ab0332471bc91d330f9c2650d37c6b852e422acb4067e45344ae0c59d2ca5806",
    "TM-3-2020/splits/train/train-ab.tsv": "6f746dd8339e3790e40a8e5168a72d2c50bc08b179e1477ecdb138b40fc29eed",
    "TM-3-2020/splits/train/train-ac.tsv": "7521d025b81e6318213c321f789bc7df61aaa393520bd429746a246c561b5fe9",
    "TM-3-2020/splits/train/train-ad.tsv": "f6e61ea099cceaa0e11f1cdbeaba8952dc3b4579d14d1ab392228b3ece5ec5b6",
    "TM-3-2020/splits/train/train-ae.tsv": "4e8aa1c8e719e4724fa00baa3834ebdd7bb93102979864dcefa5a71070608e12",
    "TM-3-2020/splits/train/train-af.tsv": "9b82d3818fa2d33568f94c22f941199ee3d1ad11401a8faabffb13780e3177b0",
    "TM-3-2020/splits/train/train-ag.tsv": "0dd2f2c7432ed5e4c54dffced214c51ddf5bd8b3b2dfc3a738b21e3f92dec13b",
    "TM-3-2020/splits/train/train-ah.tsv": "fed3a8beae3eafcc790617818d00c13e4fef6751a66816ebf38ee9a8ed63a56c",
    "TM-3-2020/splits/train/train-ai.tsv": "96647e51398612e2c225e48595dc3babd27fc9dc521155b10aada1af4a66cefc",
    "TM-3-2020/splits/train/train-aj.tsv": "27737363e11e2e267c3b68a488ccb9bf4770561c546371d913f78353e9a7414a",
    "TM-3-2020/splits/train/train-ak.tsv": "1f1ea60aa306bf2a87aef98db972f4d61081c98a07bda2e60cd422fd3b2979be",
    "TM-3-2020/splits/train/train-al.tsv": "3c53372a212820f222fa6ddd81afccf66e7ad2b3355f682760a759d295216b02",
    "TM-3-2020/splits/train/train-am.tsv": "30056caf7dfad8356ac8364b97b251a6839ac1ed1c92bd01018bab272062c0bc",
    "TM-3-2020/splits/train/train-an.tsv": "68aaa9cb029649b095e1b1115b5949f28ad77e26e592410db59b183b2af57080",
    "TM-3-2020/splits/train/train-ao.tsv": "de41328cfc8cb0852eb15bfa40588db0353c4cc9c3953691d4461c9babc8da60",
    "TM-3-2020/splits/train/train-ap.tsv": "04919afa40b2b63af048475d874ba83894b8a86115ad41630b528c14b5a8d9a5",
    "TM-3-2020/splits/train/train-aq.tsv": "f50151ff90ff074e5a7dd1f9ba212a23842512bf81593f87b52a57807b38f0f8",
    "TM-3-2020/splits/train/train-ar.tsv": "6bc1cf5091229e245db89a2f5ade4d95b0d45d847c020a45fe37754e423f8db7",
    "TM-3-2020/splits/train/train-as.tsv": "9dbda0634d1851115fccb0ff5d3c6833b16429caa906af80acfebfb8f62d2c74",
    "TM-3-2020/splits/train/train-at.tsv": "203214d9cf08ee7571ca5209ad1a0e8ef72284afdd613d19346cef64e6516c96",
    "TM-3-2020/splits/train/train-au.tsv": "38ad5ca88d251271f1d1579574e6fb46d19cbc07ac626ab0da76e02db7303699",
    "TM-3-2020/splits/train/train-av.tsv": "46655db8a2f657e96535cef2d6174ccc3c7d4df50711a62cae8cdc1efa4b1a3c",
    "TM-3-2020/splits/train/train-aw.tsv": "d9cda7438516f957e288097049498df112de4fd3cf25569e47666732c8b1de2d",
    "TM-3-2020/splits/train/train-ax.tsv": "b1adb723d6153ae1d92658b58fd9629de82a59ddddddf799635757142c01613a",
    "TM-3-2020/splits/train/train-ay.tsv": "5ee13cdd6d8cae8fe95758d0b6309468a24c92232e038ef3b12255ce8f25e4cf",
    "TM-3-2020/splits/train/train-az.tsv": "34f1f461a182c41f508e7a4ec4deba914ea8c1094d6399e483ded0290ef8fa37",
    "TM-3-2020/splits/train/train-ba.tsv": "08796e75d9f1f11ae58286ecfe2e01c72b3b872df9a594b8b716e1b25924e1fe",
    "TM-3-2020/splits/train/train-bb.tsv": "8e016d52b5697c0e9f8a2d94b3c6cf2e8a98e3cfafb4177e73cfc500345cfe81",
    "TM-3-2020/splits/train/train-bc.tsv": "d2cbf4e535edeb574a8aaec4483b0cee529e1fa8a7df8dfc27f2835061322e2b",
}


def licence(tm):
    return (f"CC BY 4.0 (https://github.com/google-research-datasets/Taskmaster/blob/{COMMIT}/{tm}/README.md "
            "'COPYRIGHT NOTICE ... made available under the Creative Commons Attribution 4.0 License')")


def fetch(rel):
    """Download one pinned Taskmaster file into the cache (sha256-verified) and return its local path."""
    path = CACHE / rel
    C.fetch(BASE + rel, path, SHA[rel])
    return path


def fetch_prefix(prefix):
    return {rel: fetch(rel) for rel in sorted(SHA) if rel.startswith(prefix)}
