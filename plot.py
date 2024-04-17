import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import mplfinance as mpf


def getDirectory(directory):
    results_download = []
    results_upload = []
    results = [results_download, results_upload]

    # Loop through files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            # Extract filename without extension
            name = os.path.splitext(filename)[0]

            # Read Excel file
            file_path = os.path.join(directory, filename)
            df = pd.read_excel(file_path)

            download_values = df['intervals_streams_bits_per_second'][1:].tolist()  # Exclude header row
            # upload_values = df['upload'][1:].tolist()  # Exclude header row

            # Combine values to dictionary
            results_download.append({f'{name}_download': download_values})
            # results_upload.append({f'{name}_upload': upload_values})

    return results

def getDataList(file):
    df = pd.read_excel(file)
    download_values = df['intervals_streams_bits_per_second'][1:].tolist()  # Exclude header row
    # upload_values = df['upload'][1:].tolist()  # Exclude header row

    return download_values

def convertToDict(key, value):
    return {key: value}

def plot_candlestick(plotTitle, *args):
    fig, axes = plt.subplots(2, 1, sharex=True)
    # set the share x axis to be true so that the x axis is shared between the two subplots
    ax = axes[0]
    ax_volume = axes[1]

    combined_data = {}
    for arg in args:
        combined_data.update(arg)
    all_data = {}
    for data_dict in args:
        for key, values in data_dict.items():
            if key not in all_data:
                all_data[key] = []

            all_data[key].extend(values)

    x_labels = list(all_data.keys())
    x_ticks = range(1, len(x_labels) + 1)

    for i, (key, values) in enumerate(all_data.items()):
        x = x_ticks[i]
        y_low = min(values)
        y_high = max(values)
        y_avg = np.mean(values)
        y_median = np.median(values)
        y_lower_q = np.percentile(values, 25)
        y_upper_q = np.percentile(values, 75)

        ax.plot([x, x], [y_low, y_high], color='black')  # Plot vertical line
        ax.plot([x - 0.1, x + 0.1], [y_avg, y_avg], color='blue', label='Average')  # Average
        ax.plot([x - 0.1, x + 0.1], [y_median, y_median], color='green', label='Median')  # Median
        ax.plot([x - 0.1, x + 0.1], [y_lower_q, y_lower_q], color='orange', label='Lower Quartile')  # Lower Quartile
        ax.plot([x - 0.1, x + 0.1], [y_upper_q, y_upper_q], color='red', label='Upper Quartile')  # Upper Quartile

        # Plot volume on the second subplot
        ax_volume.bar(x, len(values), color='gray')

    # Set labels and title for the plot
    ax.set_ylabel('Speed (bytes/s)')
    ax.set_title(plotTitle)
    ax.set_xticks(x_ticks)
    # ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.legend(['Average', 'Median', 'Lower Quartile', 'Upper Quartile'])

    # Plot volume at the bottom
    ax_volume.set_xticklabels(x_labels, rotation=45, ha='right')
    ax_volume.set_ylabel('Volume')

    plt.tight_layout()
    plt.show()


def find_xlsx_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xlsx'):
                json_files.append(os.path.join(root, file))
    return json_files



if __name__ == "__main__":
    f24_coi_ch1_db0_shield_download = convertToDict("ch1_db0_coi_download", getDataList("output/db0/f24-coi-ch1-shield-download.xlsx"))
    f24_aci_ch1_db0_shield_download = convertToDict("ch1_db0_aci_download", getDataList("output/db0/f24-aci-ch1-shield-download.xlsx"))

    # db0_download = ["db0_download"]
    # db0_upload ={}
    # for xlsx in find_xlsx_files('output\\db0'):
    #     if "download" in xlsx:
    #         fileName = xlsx.split('\\')[-1].split('.')[0].replace("f24-","")
    #         fileName = fileName.replace("-shield-download","")
    #         downloadData = convertToDict(fileName, getDataList(xlsx))
    #         db0_download.append(downloadData)
    #     elif "upload" in xlsx:
    #         fileName = xlsx.split('\\')[-1].split('.')[0].replace("f24-","")
    #         fileName = fileName.replace("-shield-upload","")
    #         uploadData = convertToDict(fileName, getDataList(xlsx))
    #         db0_upload.append(uploadData)



    # plot_candlestick(db0_download[0], db0_download[1:]))
    plot_candlestick("db0_download", f24_coi_ch1_db0_shield_download, f24_aci_ch1_db0_shield_download)
    # plot_candlestick("db0_download",f24_ni_ch1_db0_shield_download, f24_coi_ch1_db0_shield_download, f24_aci_ch1_db0_shield_download, f24_ni_ch6_db0_shield_download, f24_coi_ch6_db0_shield_download, f24_aci_ch6_db0_shield_download, f24_ni_ch11_db0_shield_download, f24_coi_ch11_db0_shield_download, f24_aci_ch11_db0_shield_download)
