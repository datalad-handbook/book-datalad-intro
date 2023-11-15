from pathlib import Path
import re
import subprocess
from urllib.parse import (
    SplitResult,
    urlsplit,
)

part = None
chap = None
outfp = None
outfile = None
mainfile = Path('main.tex').open('w')

date_regex = re.compile(r'^\\date{[^{}]+}$')
#part_regex = re.compile(r'^\\part.*{([^{}]+)}.*')
chap_regex = re.compile(r'^\\chapter{(.*)}')
sphinxhref_regex = re.compile(r'(.*)\\sphinxhref{([^}]+)}(.*)$')
footnotemark_regex = re.compile(r'(.*)\\begin{footnote}\[[0-9]+\]\\sphinxAtStartFootnote$')

excluded_parts = ['parts/introduction_whatyoureallyneedtoknow.tex',
                  'parts/advanced.tex', 'parts/advanced_advancedoptions.tex',
                  'parts/advanced_gobigorgohome.tex',
                  'parts/advanced_computingonclusters.tex',
                  'parts/advanced_betterlatethannever.tex',
                  'parts/advanced_specialpurposeshowrooms.tex',
                  'parts/advanced_dataladinternals.tex',
                  'parts/advanced_dataladextensions.tex', 'parts/usecases.tex',
                  'parts/usecases_atypicalcollaborativedatamanagementworkflow.tex',
                  'parts/usecases_basicprovenancetracking.tex',
                  'parts/usecases_writingareproduciblepaper.tex',
                  'parts/usecases_studentsupervisioninaresearchproject.tex',
                  'parts/usecases_abasicautomaticallyandcomputationallyreproducibleneuroimaginganalysis.tex',
                  'parts/usecases_anautomaticallyandcomputationallyreproducibleneuroimaginganalysisfromscratch.tex',
                  'parts/usecases_scalingup:managing80tband15millionfilesfromthehcprelease.tex',
                  'parts/usecases_buildingascalabledatastorageforscientificcomputing.tex',
                  'parts/usecases_usingglobusasadatastoreforthecanadianopenneuroscienceportal.tex',
                  'parts/usecases_encrypteddatastorageandtransport.tex',
                  'parts/usecases_contributing.tex',
]


def get_domain_from_surl(surl):
    return SplitResult(
        scheme=surl.scheme,
        netloc=surl.netloc,
        path='',
        query='',
        fragment='',
    ).geturl()


def get_links_props(path):
    groups = set()
    # orig URL to domain and SplitResult
    links = {}
    # gather all links
    for line in path.open():
        href = sphinxhref_regex.match(line)
        if not href:
            continue

        # line is what comes before the URL
        # url is just that
        # rest contains the link's display name (in {}) and whatever
        # is the trailing part of that line
        line, url, rest = href.groups()
        if url in links:
            # we know already
            continue
        # parse the URL to be able to break the link index down
        surl = urlsplit(url)
        domain = get_domain_from_surl(surl)
        groups.add(domain)
        links[url] = (domain, surl)

    # group links by domain and assign per-domain ID
    grouped = {k: set() for k in sorted(groups)}
    for domain, surl in links.values():
        if url_is_just_domain(surl, domain):
            # this URL is just the group-domain, no need for a special ID
            continue
        group = grouped[domain]
        group.add(surl)

    id_chars = 'ABCDEFGHKLMNOPQRSTUVWXYZ'
    group_ids = {
        'https://git-annex.branchable.com': ('B1', 'B01'),
        'https://docs.datalad.org': ('D1', 'D01'),
        'https://handbook.datalad.org': ('D2', 'D02'),
        'https://datasets.datalad.org': ('D3', 'D03'),
        'https://git-scm.com': ('G1', 'G01'),
        'https://github.com': ('G2', 'G02'),
        'https://docs.github.com': ('G3', 'G03'),
        'https://github.blog': ('G4', 'G04'),
        'https://gin.g-node.org': ('G5', 'G05'),
        'https://www.gnu.org': ('G6', 'G06'),
        'https://en.wikipedia.org': ('W1', 'W01'),
    }
    group_id_counts = {
        'B': 1,
        'D': 3,
        'G': 6,
        'W': 1,
    }
    for group in sorted(grouped):
        if group in group_ids:
            continue
        # get first char of domain
        id_char = urlsplit(group).netloc.split('.')[-2][0].upper()
        id_count = group_id_counts.get(id_char, 0)
        id_count += 1
        group_id_counts[id_char] = id_count
        group_ids[group] = (f'{id_char}{id_count}', f'{id_char}{id_count:02}')

    # now assign IDs, sorted by URL
    grouped = {
        domain: (
            # for sorting
            group_ids[domain][1],
            # for rendering
            group_ids[domain][0],
            {
                surl: (
                    # for sorting
                    i,
                    # for rendering
                    # was [A-Z][0-9]
                    #f'{id_chars[int((i + 1) / 10)]}{(i + 1) % 10}',
                    # now just [A-Z]; this will error out with an IndexError
                    # if we run out of letters, so no silent skipping danger
                    f'{id_chars[i]}',
                )
                for i, surl in enumerate(sorted(grouped[domain]))
            },
        )
        for d, domain in enumerate(sorted(grouped))
    }

    url2props = {
        url: dict(
            domain=domain,
            domain_idx=grouped[domain][1],
            surl=surl,
            surl_idx=None
            if url_is_just_domain(surl, domain)
            else grouped[domain][2][surl][1],
            ndomainurls=len(grouped[domain]),
        )
        for url, (domain, surl) in links.items()
    }

    return url2props, grouped


def url_is_just_domain(surl, domain):
    return surl.geturl() in (domain, f'{domain}/', f'{domain}//')


def get_refid_from_linkprops(lp):
    if lp['ndomainurls'] > 1:
        return f'{lp["domain_idx"]}{lp["surl_idx"] if lp["surl_idx"] else ""}'
    else:
        return f'{lp["domain_idx"]}'


src_latex = Path('src', 'sphinx', 'dataladhandbook.tex')
linkprops, link_groups = get_links_props(src_latex)


for line in src_latex.open():
    #part_match = part_regex.match(line)
    chap_match = chap_regex.match(line)
    #if part_match:
    #    chap = None
    #    part = part_match.group(1)
    if chap_match:
        chap = chap_match.group(1)
    elif line.startswith(r'\renewcommand{\indexname}{Index}'):
    #    part = None
        chap = None
    #outfp_new = '{}{}{}.tex'.format(
    #    (part or '').lower().replace(' ', ''),
    #    '_' if chap else '',
    #    (chap or '').lower().replace(' ', ''),
    #)
    outfp_new = '{}.tex'.format(
        (chap or '').lower().replace(' ', '').replace(r'\sphinxhyphen{}', '-'),
    )
    if outfp_new == '.tex':
        if outfp and outfp != 'preamble.tex':
            outfp_new = 'end.tex'
        else:
            outfp_new = 'preamble.tex'
            if date_regex.match(line):
                committer_date = subprocess.run(
                    ['git', 'show', '-s', '--pretty=format:%cs'],
                    cwd='src/handbook',
                    text=True,
                    capture_output=True).stdout
                line = f'\\date{{{committer_date}}}\n'
    if outfp != outfp_new:
        outfp = outfp_new
        outfile = Path('parts', outfp).open('w')
        mainfile.write('\\input{parts/%s}\n' % str(outfp))
    href = sphinxhref_regex.match(line)
    if href and outfile.name not in excluded_parts:
        # line is what comes before the URL
        # url is just that
        # rest contains the link's display name (in {}) and whatever
        # is the trailing part of that line
        line, url, rest = href.groups()
        refid = get_refid_from_linkprops(linkprops[url])
        line += '\\dlhbhref{%s}%s\n' % (refid, rest)

    if footnotemark_regex.match(line):
        # remove manual footnote labeling, always occurs on a separate line
        line = '\\begin{footnote}\\sphinxAtStartFootnote\n'
    outfile.write(line)


urlsfile = Path('hyperlink_items.tex').open('w')

for domain, (_, domain_idx, surls) in sorted(
        link_groups.items(),
        key=lambda x: x[1][0],
):
    # determine URLs for this domain
    domain_items = {}
    for surl, surl_idx in sorted(surls.items(), key=lambda x: x[0]):
        render_url = surl.geturl()
        if render_url.startswith(domain):
            render_url = f'{render_url[len(domain):]}'
        if not surl.scheme and surl.netloc:
            assert render_url[:2] == '//'
            render_url = render_url[2:]
        domain_items[surl_idx] = render_url

    if not len(domain_items):
        urlsfile.write("\\item[{}] \\url{{{}}}\n".format(
            domain_idx,
            f'{domain}',
        ))
        continue
    elif len(domain_items) == 1:
        _, item_url = domain_items.popitem()
        urlsfile.write("\\item[{}] \\url{{{}}}\n".format(
            domain_idx,
            f'{domain}{item_url}',
        ))
        continue

    urlsfile.write("\\item[{}] \\url{{{}}}\n".format(domain_idx, domain))
    # we want to nested items to appear in line with the level above
    # the indentation is coming via the longer IDs
    urlsfile.write("\\begin{description}\n\\vspace{-2mm}\n\\setlength{\itemindent}{-13mm}\n\\setlength{\\itemsep}{-2mm}\n")
    for (_, key), url in domain_items.items():
        urlsfile.write("  \\item[{}] \\url{{...{}}}\n".format(
            f'{domain_idx}{key}',
            url,
        ))
    urlsfile.write("\\end{description}\n")
