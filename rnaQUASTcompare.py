from argparse   import ArgumentParser
from datetime   import datetime
from matplotlib import patches, pyplot
from numpy      import max
from os         import path
from pandas     import concat, DataFrame, read_csv
from pathlib    import Path
from random     import choice
from re         import search

gene_metrics        = ["Genes",
                       "50%-assembled genes",
                       "95%-assembled genes",
                       "50%-covered genes",
                       "95%-covered genes"]       
isoforms_metrics    = ["Isoforms",
                       "50%-assembled isoforms",
                        "95%-assembled isoforms",
                       "50%-covered isoforms",
                        "95%-covered isoforms"]
transcripts_metrics = ["Transcripts",
                       "Transcripts > 500 bp",
                        "Transcripts > 1000 bp",
                        "Aligned",
                        "Uniquely aligned",
                        "Multiply aligned",
                        "Unaligned",
                        "Misassemblies",
                        "50%-matched",
                        "95%-matched",
                        "Unannotated",]
scaled_metrics      = ["Mean fraction of transcript matched",
                        "Mean isoform assembly",
                        "Mean isoform coverage",
                        "Database coverage",
                        "Avg. aligned fraction"]
other_metrics       = ["Avg. aligned fraction",
                       "Avg. mismatches per aligned kb",
                       "Database coverage",
                       "Duplication ratio",
                       "Mean isoform coverage",
                       "Mean isoform assembly",
                       "Mean fraction of transcript matched"]
                                                 
class MyArgumentParser(ArgumentParser):

    prog        =   "rnaQUASTcompare"

    description =   """
                    ----------\n
                    Comparing rnaQUAST reports from multiple assemblies.\n
                    Generates combined Dataframes (.csv, tsv and .tex) and plots.\n
                    """
    
    help = {
            "report_dirs": "paths to output directories from rnaQUAST",
            "names":       "list of names for the assemblies (default=[\"auto\"])",
            "colors":      "list of colors in hexcode (default=[\"auto\"])",
            "title":       "main title for plot"
        }
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)
        
        self.add_argument("report_dirs",   nargs='+', type=str, help=self.help["report_dirs"])
        self.add_argument("-n","--names",  nargs='+', type=str, help=self.help["names"],      default=[])
        self.add_argument("-c","--colors", nargs='+', type=str, help=self.help["colors"],     default=[])
        self.add_argument("-t", "--title",            type=str, help=self.help["title"],      default="")
        self.add_argument("-o","--outdir",            type=str,                               default="rnaQUASTcompare_"+
        datetime.now().strftime("%dd%mm%Yy_%Hh%Mm%Ss"))

    def arg_parse():

        args = super().argparse()

        if any(args.names) and not len(args.names)==len(args.reports_dir):
            raise Exception("Number of names must match number of reports")
        if any(args.colors) and not len(args.colors)==len(args.reports_dir):
            raise Exception("Number of colors must match number of reports")
            
        return args

class ReportParser():

    def get_number_of_isoforms(cls, file_path: str)->int:
        """
        Parameters:
            file_path (str), path of a database_metrics.txt-file
        Returns:
            (float), the number of isoforms
        """
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("Isoforms"):
                    return float(search(r'[-+]?\d*\.?\d+', line).group(0))
                
    @classmethod
    def mmpt_to_mmpkb(cls, sr: DataFrame):
        """
        Conversion of "Avg. mismatches per transcript" to "Avg. mismatches per aligned kb" 

        Args:
            sr (DataFrame): rnaQUAST short report
        """
        
        av_al = float(sr.loc[sr["metrics"]=="Avg. alignment length",sr.columns[1]].iloc[0])
        av_mm = float(sr.loc[sr["metrics"]=="Avg. mismatches per transcript",sr.columns[1]].iloc[0])

        i = sr.loc[sr["metrics"]=="Avg. mismatches per transcript"].index
        sr.loc[i,"metrics"]     = "Avg. mismatches per aligned kb"
        sr.loc[i,sr.columns[1]] = 1000 * av_mm / av_al
    
    def parse_report(cls, report_dir):

        # Loading short report
        report = read_csv(path.join(report_dir, "short_report.tsv"), sep="\t")
        report.rename(columns={'METRICS/TRANSCRIPTS': 'metrics'}, inplace=True)

        # Adding the number of isoforms from the reference
        file_path = path.join(report_dir, report.columns[1]+"_output")
        file_path = path.join(file_path, "database_metrics.txt")
        new_row   = DataFrame({"metrics": ["Isoforms"],
                               report.columns[1]: [cls.get_number_of_isoforms(file_path)]})
        report    = concat([report.iloc[:2], new_row, report.iloc[2:]]).reset_index(drop=True)

        # Converting "Avg. mismatches per transcript" to "Avg. mismatches per aligned kb"
        cls.mmpt_to_mmpkb(report)

        return report

class ValueScaler():

    @classmethod
    def find_divider(cls, reports: list[DataFrame], j: int, metric: str)->float:

        report = reports[j]

        if metric in gene_metrics:
            return float(report.loc[report["metrics"]=="Genes"][report.columns[1]].iloc[0])
        if metric in isoforms_metrics:
            return float(report.loc[report["metrics"]=="Isoforms"][report.columns[1]].iloc[0])
        if metric in transcripts_metrics:
            return float(report.loc[report["metrics"]=="Transcripts"][report.columns[1]].iloc[0])
        if metric in scaled_metrics:
            return 1
        return max([float(sr.loc[sr["metrics"]==metric,sr.columns[1]].iloc[0]) for sr in reports])
    
    @classmethod
    def get_scaled_values(cls, reports: list[DataFrame], j: int)->list[float]:

        scaled_values = []

        for i in range(reports[j].shape[0]):

            metric  = reports[j]["metrics"].iloc[i]
            value   = float(reports[j][reports[j].columns[1]].iloc[i])
            divider = cls.find_divider(reports, j, metric)

            scaled_values.append(value / float(divider))

        return scaled_values

def latex_format(data: DataFrame):

    copy = data.copy()

    for i in range(copy.shape[0]):
        copy.loc[i,"metrics"] = str(copy.loc[i,"metrics"]).replace("%","\\%")
    
    return copy

def store_data(data: DataFrame, save_as: str):

    data.to_csv(save_as+".csv")
    data.to_csv(save_as+".tsv", sep="\t")
    latex_format(data).style.to_latex(save_as+".tex")

def data_preprocessing(args):
    """
    Loads, combines and scales
    """

    reports = [ReportParser().parse_report(report_dir) for report_dir in args.report_dirs]

    if any(args.names):
        names = args.names
    else:
        names = [sr.columns[1] for sr in reports]

    if any(args.names):

        combined = DataFrame({"metrics": reports[0]['metrics']})

        for i, sr in enumerate(reports):
            combined[names[i]] = sr[sr.columns[1]]
        save_as = path.join(args.outdir, "combined_data_absolutes")
        store_data(combined, save_as)
        
        """
        for i, sr in enumerate(reports):
            combined[names[i]+' (scaled)']   = ValueScaler().get_scaled_values(reports, i)
        save_as = path.join(args.outdir, "combined_data_all")
        store_data(combined, save_as)
        """
        
    return combined

class Plotter():

    @classmethod
    def empty_subplot(cls, axes, metrics, title):

        for tick in axes.get_xticks():
            axes.axvline(x=tick, color='gray', linestyle='--', alpha=0.5)
        axes.tick_params(axis='x', which='major', labelsize=30)
        axes.set_yticks(list(range(len(metrics))))
        axes.set_yticklabels(metrics, fontweight='bold', fontsize=30)
        axes.set_ylim(ymin=-0.5,ymax=len(metrics)-0.5)

        axes.grid(axis='y', linestyle='--', linewidth=0.5)
        axes.set_title(title, fontweight='bold', fontsize=30)

    def fill_lines(cls, axes, data, metrics, colors):
    
        xmax = 0
        for i, assembly in enumerate(data.columns[1:]):
            x = data.loc[data["metrics"].isin(metrics)][assembly]
            xmax = max([max(x),xmax])
            axes.plot(x, range(x.shape[0]), c=colors[i], linewidth=3)

        axes.set_xlim(xmin=0,xmax=xmax)
        axes.set_xticklabels(axes.get_xticks(), rotation=45)

    def get_colors(cls, args):

        if any(args.colors):
            return args.colors
        else:
            return ["#"+"".join([choice("0123456789abcdef") for _ in range(6)])
                    for _ in args.report_dirs]
   
    def plot(cls, data, args):

        fig, axes = pyplot.subplots(2,2, figsize=(25,20))

        fig.suptitle(args.title, fontweight="bold", fontsize=40)

        pyplot.subplots_adjust(wspace=7/4, hspace=2/4)

        cls.empty_subplot(axes[0][0], gene_metrics,         "Gene metrics")
        cls.empty_subplot(axes[0][1], transcripts_metrics,  "Transcript metrics")
        cls.empty_subplot(axes[1][0], isoforms_metrics,     "Isoform metrics")
        cls.empty_subplot(axes[1][1], other_metrics,        "Other metrics")

        colors = cls.get_colors(args) # args.colors if set, else random colors
        
        cls.fill_lines(axes[0][0], data, gene_metrics,        colors)
        cls.fill_lines(axes[0][1], data, transcripts_metrics, colors)
        cls.fill_lines(axes[1][0], data, isoforms_metrics,    colors)
        cls.fill_lines(axes[1][1], data, other_metrics,       colors)

        pyplot.legend([patches.Rectangle([0,0],5,5,color=c) for c in colors],
                      data.columns[1:],
                      bbox_to_anchor=(-9, -2.25, 5, 5),
                      fontsize=30)

        pyplot.savefig(path.join(args.outdir,"plot"),
                       bbox_inches='tight',
                       pad_inches=0.5)

def main():

    args = MyArgumentParser().parse_args()

    # Create outputfolder
    Path(args.outdir).mkdir(parents=True)

    # Load / preprocess 
    data = data_preprocessing(args)

    print(data)

    Plotter().plot(data,args)

if __name__ == '__main__':
    
    main()
