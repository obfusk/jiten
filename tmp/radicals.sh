for x in {1..214}; do
  echo $x
  curl -s -- "https://en.wikipedia.org/wiki/Radical_$x" \
    | ( grep -E -A5 '>(without|0|no)( additional)? strokes|>0(<|$)|\+ ?0(<|$)' || echo ) \
    | tail -n +2 | tr '\n' ' ' | sed 's!</tr>.*!!' \
    | tr -d '0-9A-Za-z"=<> :/.%#()+_&;?,-'
  echo
done
