# This input file tests the behavior of Navier-Stokes equations

[GlobalParams]
  gravity = '0 0 0'
  laplace = true
  integrate_p_by_parts = false
  pspg = true
  alpha = 1
  convective_term = false
[]

[Mesh]
  block_name = 'rock voids'
  block_id = '0 1'
  #boundary_name = grains
  #boundary_id = 10
 [generated]
    type = GeneratedMeshGenerator
    dim = 3
    nx = 30
    ny = 30
    nz = 30
  []
  [./image]
    input = generated
    type = ImageSubdomainGenerator
    file = /path/to/file/
    threshold = 100
  [../]
  [./interface]
    type = SideSetsBetweenSubdomainsGenerator
    input = image
    primary_block = 1
    paired_block = 0
    new_boundary = 10
  [../]
  [rename]
    type = RenameBoundaryGenerator
    input = interface
    old_boundary = 10
    new_boundary = 'grains'
  []
  [./delete]
    type = BlockDeletionGenerator
    input = rename
    block = 0
  [../]
  [./box]
    type = SubdomainBoundingBoxGenerator
    bottom_left = '0.05 0.05 0.05'
    top_right = '0.95 0.95 0.95'
    block_id = 2
    input = mesh
  [../]
[]

[Variables]
  [./vel_x]
  [../]
  [./vel_y]
  [../]
  [./vel_z]
  [../]
  [./p]
  [../]
[]

[Kernels]
  [./mass]
    type = INSMass
    variable = p
    u = vel_x
    v = vel_y
    w = vel_z
    pressure = p
  [../]
  [./x_momentum_space]
    type = INSMomentumLaplaceForm
    variable = vel_x
    u = vel_x
    v = vel_y
    w = vel_z
    pressure = p
    component = 0
  [../]
  [./y_momentum_space]
    type = INSMomentumLaplaceForm
    variable = vel_y
    u = vel_x
    v = vel_y
    w = vel_z
    pressure = p
    component = 1
  [../]
  [./z_momentum_space]
    type = INSMomentumLaplaceForm
    variable = vel_z
    u = vel_x
    v = vel_y
    w = vel_z
    pressure = p
    component = 2
  [../]
[]

[AuxVariables]
  [./gradP_x]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./gradP_y]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./gradP_z]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./product]
    family = MONOMIAL
    order = CONSTANT
  [../]
[]

[AuxKernels]
  [./gradP_x_aux]
    type = VariableGradientComponent
    variable = gradP_x
    gradient_variable = p
    component = x
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [./gradP_y_aux]
    type = VariableGradientComponent
    variable = gradP_y
    gradient_variable = p
    component = y
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [./gradP_z_aux]
    type = VariableGradientComponent
    variable = gradP_z
    gradient_variable = p
    component = z
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [./product]
    type = ParsedAux
    variable = product
    args = 'gradP_x gradP_y gradP_z vel_x vel_y vel_z'
    function = 'vel_x*gradP_x+vel_y*gradP_y+vel_z*gradP_z'
  [../]
[]

[Materials]
  [./const]
    type = GenericConstantMaterial
    prop_names = 'rho mu'
    prop_values = '1  1'
  [../]
[]

[Functions]
  [perm_f]
    # length of sample is 170 voxels and resolution of image is 10.002 micrometer and we want perm in Darcy
    type = ParsedFunction
    value = 'phi*v*(170*10.002e-6)^2/9.86e-13'
    vals = 'vol velx_avg'
    vars = 'phi v'
  []
  [linear_p]
    type = ParsedFunction
    value = '1-x'
  []
[]

[ICs]
  [linear_p]
    type = FunctionIC
    function = linear_p
    variable = p
  []
[]

[BCs]
  [./x_no_slip]
    type = DirichletBC
    variable = vel_x
    boundary = 'grains back front top bottom'
    value = 0.0
  [../]
  [./y_no_slip]
    type = DirichletBC
    variable = vel_y
    boundary = 'grains back front top bottom'
    value = 0.0
  [../]
  [./z_no_slip]
    type = DirichletBC
    variable = vel_z
    boundary = 'grains back front top bottom'
    value = 0.0
  [../]
  [./lowp]
    type = DirichletBC
    variable = p
    boundary = 'right'
    value = 0
  [../]
  [./inlet]
    type = DirichletBC
    variable = p
    boundary = 'left'
    value = 1
  [../]
[]

[Postprocessors]
  # active = 'vol perm_in perm integral_in integral_out vel_avg'
  [./vol]
    type = VolumePostprocessor
    execute_on = initial
    # block = 2
  [../]
  [./area]
    type = AreaPostprocessor
    execute_on = initial
    boundary = grains
  [../]
  [./integral_in]
    type = SideIntegralVariablePostprocessor
    variable = vel_x
    boundary = left
  [../]
  [./integral_out]
    type = SideIntegralVariablePostprocessor
    variable = vel_x
    boundary = right
  [../]
  [./velx_avg]
    type = ElementAverageValue
    variable = vel_x
    block = 2
  [../]
  [./velx_int]
    type = ElementIntegralVariablePostprocessor
    variable = vel_x
    block = 2
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [./vely_avg]
    type = ElementAverageValue
    variable = vel_y
    block = 2
  [../]
  [./vely_int]
    type = ElementIntegralVariablePostprocessor
    variable = vel_y
    block = 2
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [./velz_avg]
    type = ElementAverageValue
    variable = vel_z
    block = 2
  [../]
  [./velz_int]
    type = ElementIntegralVariablePostprocessor
    variable = vel_z
    block = 2
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [./gradPx_avg]
    type = ElementAverageValue
    variable = gradP_x
    block = 2
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [./gradPy_avg]
    type = ElementAverageValue
    variable = gradP_y
    block = 2
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [./gradPz_avg]
    type = ElementAverageValue
    variable = gradP_z
    block = 2
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [permeability]
    type = FunctionValuePostprocessor
    function = perm_f
  []
  [./product_avg]
    type = ElementAverageValue
    variable = product
    block = 2
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [./product_int]
    type = ElementIntegralVariablePostprocessor
    variable = product
    block = 2
    execute_on = 'INITIAL TIMESTEP_END'
  [../]
  [mem]
    type = MemoryUsage
    mem_type = physical_memory
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [./dofs]
    type = NumDOFs
    execute_on = 'initial timestep_end'
  [../]
[]

[Executioner]
  # This is setup automatically in MOOSE (SetupPBPAction.C)
  # petsc_options = '-snes_mf_operator'
  # petsc_options_iname = '-pc_type'
  # petsc_options_value =  'asm'
  # petsc_options_iname = '-pc_type -pc_asm_overlap -sub_pc_type -sub_pc_factor_levels'
  # petsc_options_value = 'asm      2               ilu          4'
  # line_search = 'none'
  # nl_rel_tol = 1e-12
  # nl_abs_tol = 1e-13
  # nl_max_its = 6
  # l_tol = 1e-6
  # l_max_its = 500
  # Solver tolerances and iteration limits
  # nl_rel_tol = 1e-8
  # nl_abs_tol = 1e-12
  # nl_max_its = 10
  # l_tol = 1e-6
  # l_max_its = 50 #10
  # line_search = none
  # # Options passed directly to PETSc
  # petsc_options = '-snes_converged_reason -ksp_converged_reason '
  # petsc_options_iname = '-pc_type -pc_factor_shift_type -pc_factor_mat_solver_package '
  # petsc_options_value = 'lu NONZERO superlu_dist '
  type = Steady
[]

[Preconditioning]
  inactive = 'SMP_PJFNK asm_ilu'
  [./SMP_PJFNK]
    type = SMP
    full = true
    solve_type = 'NEWTON'
  [../]
  [./FSP]
    # It is the starting point of splitting
    type = FSP
    petsc_options = '-ksp_converged_reason -snes_converged_reason'
    petsc_options_iname = '-snes_type -ksp_type -ksp_rtol -ksp_atol -ksp_max_it -snes_atol -snes_rtol -snes_max_it -snes_max_funcs'
    petsc_options_value = 'newtonls     fgmres     1e-2     1e-15       200       1e-9        1e-15       200           100000'
    topsplit = uv
    [./uv]
      # Generally speaking, there are four types of splitting we could choose
      # <additive,multiplicative,symmetric_multiplicative,schur>
      # An approximate solution to the original system
      # | A_uu  A_uv | | u | _ |f_u|
      # |  0    A_vv | | v | - |f_v|
      # is obtained by solving the following subsystems
      # A_uu u = f_u and A_vv v = f_v
      # If splitting type is specified as schur, we may also want to set more options to
      # control how schur works using PETSc options
      # multiplicative
      petsc_options_iname = '-pc_fieldsplit_schur_fact_type -pc_fieldsplit_schur_precondition'
      petsc_options_value = 'upper selfp'
      splitting = 'u v' # 'u' and 'v'
      splitting_type = schur
    [../]
    [./u]
      # PETSc options for this subsolver
      # A prefix will be applied, so just put the options for this subsolver only
      vars = 'vel_x vel_y vel_z'
      petsc_options_iname = '-pc_type -ksp_type -pc_hypre_type'
      petsc_options_value = '  hypre    preonly     boomeramg '
    [../]
    [./v]
      # PETSc options for this subsolver
      vars = p
      petsc_options_iname = '-pc_type -ksp_type -sub_pc_type -sub_pc_factor_levels'
      petsc_options_value = '  jacobi  preonly        ilu            3'
    [../]
  [../]
  [./asm_ilu]
    type = SMP
    full = true
    solve_type = PJFNK
    petsc_options = '-ksp_converged_reason -snes_converged_reason' #-snes_monitor -snes_linesearch_monitor -ksp_monitor'
    petsc_options_iname = '-ksp_type -pc_type  -snes_atol -snes_rtol -snes_max_it -ksp_max_it -ksp_atol -sub_pc_type -sub_pc_factor_shift_type'
    petsc_options_value = 'gmres        asm        1E-8      1E-15        200        100         1e-8        lu                   NONZERO'
  [../]
[]
#[Problem]
#  type = FEProblem
#  material_coverage_check = false
#  kernel_coverage_check = false
#[]

[Outputs]
  file_base = perm_ctscan_LV60A_L50 #output, check the file directory and name, generates an 'out'.e
  csv = true
  exodus = true
  perf_graph = true
[]
