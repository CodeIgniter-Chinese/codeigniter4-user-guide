#!/bin/bash

git config --global user.name "Travis-CI"
git config --global user.email "support@codeigniter.org.cn"
git clone --branch=gh-pages "https://${GH_TOKEN}@${GH_REF}" gh-pages
cd ./build/html
rm .buildinfo
zip -r ./codeigniter_user_guide.zip ./
#cd ../latex
#cp CodeIgniter.pdf ../../gh-pages/
cd ../../gh-pages
cp -Rf ../build/html/* .
git add -f .
git commit -m "Deploy to GitHub Pages"
git push -fq origin gh-pages
