# FILEPATH="data/"downloaded_`date +%Y_%m_%d`/
FILEPATH=$1

mkdir -p $FILEPATH

cd $FILEPATH

wget 'ftp://ftp.fec.gov/FEC/2014/indiv14.zip'
wget 'ftp://ftp.fec.gov/FEC/2014/cn14.zip'
wget 'ftp://ftp.fec.gov/FEC/2014/ccl14.zip'
wget 'ftp://ftp.fec.gov/FEC/2014/oth14.zip'
wget 'ftp://ftp.fec.gov/FEC/2014/pas214.zip'
wget 'ftp://ftp.fec.gov/FEC/2014/opexp14.zip'

wget -O 'CampaignAndCommitteeSummary.csv' 'http://www.fec.gov/data/CampaignAndCommitteeSummary.do?format=csv'

unzip '*.zip'
rm *.zip

YEARS="_2013_2014"
mv 'itcont.txt' 'itcont.txt'$YEARS'.txt'
mv 'itoth.txt' 'itoth'$YEARS'.txt'
mv 'cm.txt' 'cm'$YEARS'.txt'
mv 'cn.txt' 'cn'$YEARS'.txt'
mv 'ccl.txt' 'ccl'$YEARS'.txt'
mv 'itpas2.txt' 'itpas2'$YEARS'.txt'
mv 'opexp.txt' 'opexp'$YEARS'.txt'
mv 'CampaignAndCommitteeSummary.csv' 'CampaignAndCommitteeSummary'$YEARS'.csv'
