# Standard library imports
import time
import os

# Third party imports
import pandas as pd

# Local application/library imports
import setup

start = time.time()

parent_dir = os.getcwd()
path_downloaded_files = os.path.join(parent_dir, setup.DATA_DIRECTORY_NAME)

try:
    os.makedirs(setup.CSV_IN_ONE_FILE_DIRECTORY_NAME)
    print(f"\n[INFO] Creating directory: '{setup.CSV_IN_ONE_FILE_DIRECTORY_NAME}'...")
except FileExistsError:
    print(
        f"\n[INFO] Directory '{setup.CSV_IN_ONE_FILE_DIRECTORY_NAME}' already exist..."
    )
    pass


db = pd.DataFrame(
    columns=[
        "DEPARTAMENTO",
        "MUNICIPIO",
        "AGENTE COMERCIALIZADOR",
        "NIVEL TENSION",
        "DIA",
        "DEMANDA",
        "PRECIO",
    ]
)

months = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}

count_input = 0

for filename in os.listdir(path_downloaded_files):

    count_input += 1
    print(
        f"[INFO] Processing a file named '{filename}' {count_input}/{len(os.listdir(path_downloaded_files))}"
    )

    file = pd.read_excel(
        os.path.join(path_downloaded_files, filename), sheet_name=0, header=None
    )

    positions = list()

    result = file.isin(["DEPARTAMENTO"])
    columns = result.any()

    true_columns = list(columns[columns == True].index)

    for col in true_columns:

        rows = list(result[col][result[col] == True].index)

        for row in rows:
            positions.append((row, col))

    file = file.iloc[positions[0][0] :, positions[0][1] :]

    new_header = list(file.iloc[0])

    new_header2 = [
        str(col)
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("\n", "")
        .replace(" DE ", " ")
        .upper()
        for col in new_header
    ]

    file = file[1:]
    file.columns = new_header2
    file = file[
        [
            "DEPARTAMENTO",
            "MUNICIPIO",
            "AGENTE COMERCIALIZADOR",
            "NIVEL TENSION",
            "CONCEPTO",
        ]
        + [col for col in file.columns if "DIA" in str(col)]
    ].reset_index(drop=True)

    file = pd.melt(
        file,
        id_vars=[
            "DEPARTAMENTO",
            "MUNICIPIO",
            "AGENTE COMERCIALIZADOR",
            "NIVEL TENSION",
            "CONCEPTO",
        ],
        value_vars=[col for col in file.columns if "DIA" in str(col)],
        var_name="DIA",
    )

    file["DIA"] = file.apply(lambda x: x["DIA"].replace("DIA ", ""), axis=1)

    file = file.pivot_table(
        index=[
            "DEPARTAMENTO",
            "MUNICIPIO",
            "AGENTE COMERCIALIZADOR",
            "NIVEL TENSION",
            "DIA",
        ],
        columns="CONCEPTO",
        values="value",
        aggfunc="first",
    ).reset_index()

    file.rename(
        columns={
            "Demanda Diaria GWh": "DEMANDA",
            "Precio Promedio Diario ($/kWh)": "PRECIO",
        },
        inplace=True,
    )

    file["FECHA"] = (
        int("20" + filename.split(".")[0][-2:]) * 100
        + months[filename.split(".")[0].split("_")[0].lower()]
    ) * 100 + file["DIA"].astype(int)

    db = db.append(file, ignore_index=True)


db["NIVEL TENSION"] = db.apply(
    lambda x: str(x["NIVEL TENSION"]).replace("STN", "5"), axis=1
)
db = db.astype({"PRECIO": float, "DEMANDA": float, "FECHA": int, "NIVEL TENSION": int})

db.to_csv(os.path.join(setup.CSV_IN_ONE_FILE_DIRECTORY_NAME, "data.csv"), index=False)

end = time.time()

if end >= 60:
    print(
        "[INFO] Elapsed time on execution: {:.2f} minutes...".format((end - start) / 60)
    )
else:
    print("[INFO] Elapsed time on execution: {:.2f} seconds...".format(end - start))
