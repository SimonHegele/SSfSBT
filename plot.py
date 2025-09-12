files = ["rattle_lordec_trim_05m.fasta/",
         "rattle_05m.fasta/", 

         "rnabloom_sr.fasta/",
         "rnabloom_lordec_trim_05m.fasta/",
         "rnabloom_lr_05m.fasta/",
         
         "spades_sr.fasta/",
         "spades_lordec_trim_05m.fasta/",
         
         "stringtie_sr.fasta/",
         "stringtie_lordec_trim_05m.fasta/",
         "stringtie_lr_05m.fasta/",
         
         "trinity_sr.fasta/",
         "trinity_lordec_trim_05m.fasta/"]

name  = {"rattle_lordec_trim_05m.fasta/":       "RATTLE (hybrid)",
         "rattle_05m.fasta/":                   "RATTLE (lr)",
         
         "rnabloom_sr.fasta/":                  "RNA-Bloom (sr)",
         "rnabloom_lordec_trim_05m.fasta/":     "RNA-Bloom (hybrid)",
         "rnabloom_lr_05m.fasta/":              "RNA-Bloom (lr)",
         
         "spades_sr.fasta/":                    "SPAdes (sr)",
         "spades_lordec_trim_05m.fasta/":       "SPAdes (hybrid)",
         
         "stringtie_sr.fasta/":                 "StringTie (sr)",
         "stringtie_lordec_trim_05m.fasta/":    "StringTie (hybrid)",
         "stringtie_lr_05m.fasta/":             "StringTie (lr)",
         
         "trinity_sr.fasta/":                   "Trinity (sr)",
         "trinity_lordec_trim_05m.fasta/":      "Trinity (hybrid)"}

color = {"rattle_lordec_trim_05m.fasta/":       "#cc0000",
         "rattle_05m.fasta/":                   "#ff0000",
         
         "rnabloom_sr.fasta/":                  "#009900",
         "rnabloom_lordec_trim_05m.fasta/":     "#00cc00",
         "rnabloom_lr_05m.fasta/":              "#00ff00",
         
         "spades_sr.fasta/":                    "#000099",
         "spades_lordec_trim_05m.fasta/":       "#0000cc",
         
         "stringtie_sr.fasta/":                 "#000000",
         "stringtie_lordec_trim_05m.fasta/":    "#666666",
         "stringtie_lr_05m.fasta/":             "#cccccc",
         
         "trinity_sr.fasta/":                   "#990099",
         "trinity_lordec_trim_05m.fasta/":      "#cc00cc"}

names  = " ".join(["\""+name[file] +"\"" for file in files])
colors = " ".join(["\""+color[file]+"\"" for file in files])
files  = " ".join(files)

command = f"python rnaQUASTcompare.py {files} -n {names} -c {colors}"

from subprocess import run

result = run(command,
             shell=True,
             capture_output=True,
             text=True)

if result.returncode != 0:
    print("Error message:", result.stderr)
else:
    print("Output:", result.stdout)