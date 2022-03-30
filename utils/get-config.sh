function get_config {
  local ret
  ret=`python -c "import yaml; data=yaml.load(open('$1'), Loader=yaml.FullLoader); print(data['cromwell']['$2'])"`
  echo "$ret"
}
