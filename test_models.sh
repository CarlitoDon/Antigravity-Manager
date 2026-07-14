#!/bin/bash
curl -s http://localhost:8045/v1/models -H "Authorization: Bearer sk-ef1d0aadbca4446eaa1cda3710af8994" | jq -r '.data[].id' > models.txt

echo "Found $(wc -l < models.txt) models."
echo ""

while IFS= read -r model; do
  echo "--- Testing $model ---"
  for i in {1..3}; do
    echo -n "Test $i: "
    res=$(curl -s -X POST http://localhost:8045/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer sk-ef1d0aadbca4446eaa1cda3710af8994" \
      -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"say hi\"}],\"max_tokens\":10}")
    
    msg=$(echo "$res" | jq -r 'if .choices then .choices[0].message.content else .error // "Raw: \(. | tostring)" end' 2>/dev/null)
    
    if [ -z "$msg" ]; then
        msg=$(echo "$res" | head -c 100)
    fi
    
    # Trim newlines for cleaner output
    echo "$msg" | tr '\n' ' '
    echo ""
  done
  echo ""
done < models.txt
