from argparse   import ArgumentParser
from json       import load
from logging    import basicConfig, error, info, INFO, StreamHandler, warning
from matplotlib import pyplot, patches
from numpy      import array
from os         import listdir
from os.path    import commonpath, isdir, join, relpath
from pandas     import DataFrame
from sys        import stdout

class MyArgumentParser(ArgumentParser):

    prog        =   "busco_merge"

    description =   """
                    Merging BUSCO results from several assemblies
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("busco_folder",
                          help="A folder containing BUSCO output folders")

def load_reports(busco_folder: str) -> list[dict]:

    report_file_paths = []
    reports           = []

    def get_report_file_paths():

        for sub_dir_name in listdir(busco_folder):
            sub_dir_path = join(busco_folder, sub_dir_name)

            if not isdir(sub_dir_path):
                continue

            for file_name in listdir(sub_dir_path):
                if file_name.startswith("short_summary.") and file_name.endswith(".json"):
                    report_file_paths.append(join(sub_dir_path, file_name))
                    break

        return reports
    
    def load_from_files():

        for report_file_path in report_file_paths:

            with open(report_file_path) as report_file:

                reports.append(load(report_file))
  
    def check_reports():

        if len(reports) == 0:
            error("No reports found!")
            exit(1)

        lineages = [report["parameters"]["lineage_dataset"] for report in reports]

        if not len(set(lineages)) == 1:
            warning("BUSCO were results evaluated using different lineages")
    
    get_report_file_paths()
    load_from_files()
    check_reports()

    return reports

def compile_dataframe(reports):

    file_paths    = [report["parameters"]["in"] for report in reports]
    trimmed_paths = [relpath(path, commonpath(file_paths)) for path in file_paths]

    data = {"file":     trimmed_paths,
            "C":        [report["results"]["Complete BUSCOs"]        for report in reports],
            "C %":      [report["results"]["Complete percentage"]    for report in reports],
            "C (s)":    [report["results"]["Single copy BUSCOs"]     for report in reports],
            "C (S) %":  [report["results"]["Single copy percentage"] for report in reports],
            "C (M)":    [report["results"]["Multi copy BUSCOs"]      for report in reports],
            "C (M) %":  [report["results"]["Multi copy percentage"]  for report in reports],
            "F":        [report["results"]["Fragmented BUSCOs"]      for report in reports],
            "F %":      [report["results"]["Fragmented percentage"]  for report in reports],
            "M":        [report["results"]["Missing BUSCOs"]         for report in reports],
            "M %":      [report["results"]["Missing percentage"]     for report in reports],
                 }
    
    cols = ["C","C (s)","C (M)","F","M","C %","C (S) %","C (M) %","F %","M %","file"]
    
    return DataFrame(data, columns=cols)

def plot(data: DataFrame, busco_folder: str):

    fig, axes = pyplot.subplots()
    colors    = ['#0000ff','#add8e6', '#ffff00', '#ff0000']

    def formatting():
        handles = [patches.Rectangle([0,0],5,5,color=c) for c in colors]
        labels  = ('complete, single','complete, duplicated', 'fractionized', 'missing')
        axes.set_title(f"BUSCO results\n({busco_folder})")
        axes.set_yticks([i+0.5 for i in range(len(data))])
        axes.set_yticklabels(data["file"])
        axes.legend(handles, labels,
                    bbox_to_anchor=(0, -0.1, 0, 0),
                    fontsize=15)
              
    def plotting():
        for y, row in data.iterrows():
            x = array([row["C (S) %"], row["C (M) %"], row["F %"], row["M %"]])
            x = [sum(x[:i+1]) for i in range(len(x))]
            for i in range(len(x)-1,-1,-1):
                axes.barh([y+0.5], width=x[i],
                        color  = colors[i],
                        height = 0.7)
                
    def storing():
        pyplot.savefig(join(busco_folder, "merged_busco_results.png"),
                       dpi = 400,
                       bbox_inches = "tight")
        
    formatting()
    plotting()
    storing()

    pyplot.show()

def main():

    basicConfig(level = INFO,
                format   = "%(asctime)s %(levelname)s %(message)s",
                datefmt  = "%d-%m-%Y %H:%M:%S",
                handlers = [StreamHandler(stream=stdout)]
                )

    busco_folder = MyArgumentParser().parse_args().busco_folder

    reports   = load_reports(busco_folder)
    dataframe = compile_dataframe(reports)

    plot(dataframe, busco_folder)
    dataframe.to_csv(join(busco_folder, "merged_busco_results.tsv"), sep="\t")

if __name__ == "__main__":
    main() 