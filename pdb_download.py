import os
import sys
import urllib.request as request
from tqdm import tqdm

from mdhbond import HbondAnalysis


def download_pdb(pdbcode, datadir='', downloadurl="https://files.rcsb.org/download/"):
    """
    Downloads a PDB file from the Internet and saves it in a data directory.
    :param pdbcode: The standard PDB ID e.g. '3ICB' or '3icb'
    :param datadir: The directory where the downloaded file will be saved
    :param downloadurl: The base PDB download URL, cf.
        `https://www.rcsb.org/pages/download/http#structures` for details
    :return: the full path to the downloaded PDB file or None if something went wrong
    """
    pdbfn = pdbcode + ".pdb"
    url = downloadurl + pdbfn
    outfnm = os.path.join(datadir, pdbfn)
    try:
        request.urlretrieve(url, outfnm)
        return outfnm
    except Exception as err:
        print(str(err), file=sys.stderr)
        return None

def create_graph(pdb_file):
    hba = HbondAnalysis('protein', pdb_file, residuewise=False, additional_acceptors=['O'], additional_donors=['N'],
                           add_donors_without_hydrogen=True, trajectories=None, check_angle=False)
    # hba.set_hbonds_in_selection()
    hba.set_hbonds_in_selection_and_water_around(3 * 3.5)
    print(hba.initial_results)
    hba.draw_graph(use_filtered=True, draw_edge_occupancy=False, draw_labels=False, filename=f'{pdb_file[:-4]}.jpg')
    # os.remove(pdb_file)

with open('pdb_ids.txt', 'r') as f:
    pdb_ids_list = f.read().split(',')

num_of_pdbs = 10
for pdb_id in tqdm(pdb_ids_list[:num_of_pdbs]):
    print(f'>>> {pdb_id} <<<   STARTED')
    download_pdb(pdb_id)
    try:
        create_graph(f'{pdb_id}.pdb')
    except ValueError:
        print('FAILED DUE TO VALUE ERROR')
    print(f'>>> {pdb_id} <<< PROCESSED')
