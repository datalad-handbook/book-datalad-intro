all: figures

figures: \
  amend_bw.pdf \
  clouds_bw.pdf \
  collaboration_sketch_bw.pdf \
  data_origin_bw.pdf \
  datasets_bw.pdf \
  dataset_ops_bw.pdf \
  dataset_modules_bw.pdf \
  debug_bw.pdf \
  decentralized_publishing_bw.pdf \
  design_objectives_bw.pdf \
  forward_bw.pdf \
  gitidentity_bw.pdf \
  git_branch_HEAD_bw.pdf \
  git_vs_gitannex_bw.pdf \
  going_up_bw.pdf \
  help_bw.pdf \
  install_bw.pdf \
  interior_design_bw.pdf \
  keeptrack_bw.pdf \
  local_wf_bw.pdf \
  personal_settings_bw.pdf \
  publishing_network_publishparts2_bw.pdf \
  pull_request_bw.pdf \
  reading_bw.pdf \
  remote_designteam_bw.pdf \
  reproduced_bw.pdf \
  right_direction_bw.pdf \
  run_bw.pdf \
  security_bw.pdf \
  settings_bw.pdf \
  startingpoint_bw.pdf \
  student_bw.pdf \
  teacher_bw.pdf \
  typewriter_bw.pdf \
  versioncontrol_bw.pdf \
  virtual_dstree_dl101_midterm_bw.pdf \
  virtual_dstree_dl101_bw.pdf \
  warning_bw.pdf \
  yoda_bw.pdf

# black&white figures are local
%_bw.pdf: %_bw.svg
	inkscape --export-dpi=300 --export-filename "$@" "$<"

%.pdf: ../src/handbook/docs/artwork/src/%.svg
	inkscape --export-dpi=300 --export-filename "$@" "$<"

clean:
	-rm *.pdf

.PHONY: all figures clean
