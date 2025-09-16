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
  [./mesh]
    type = FileMeshGenerator
    file = Meshes/centers_0005_0002.msh
  [../]
  [./box]
    type = SubdomainBoundingBoxGenerator
    bottom_left = '0.05 0.05 0'
    top_right = '0.95 0.95 0'
    block_id = 2
    input = mesh
  [../]
[]

[Kernels]
  [./mass]
    type = INSMass
    variable = p
    u = vel_x
    v = vel_y
    pressure = p
  [../]
  [./x_momentum_space]
    type = INSMomentumLaplaceForm
    variable = vel_x
    u = vel_x
    v = vel_y
    pressure = p
    component = 0
  [../]
  [./y_momentum_space]
    type = INSMomentumLaplaceForm
    variable = vel_y
    u = vel_x
    v = vel_y
    pressure = p
    component = 1
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
  [./product]
    type = ParsedAux
    variable = product
    args = 'gradP_x gradP_y vel_x vel_y'
    function = 'vel_x*gradP_x+vel_y*gradP_y'
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
    boundary = 'grains top bottom'
    value = 0.0
  [../]
  [./y_no_slip]
    type = DirichletBC
    variable = vel_y
    boundary = 'grains top bottom' 
    value = 0.0
  [../]
  [./lowp]
    type = DirichletBC
    variable = p
    boundary = 'left' #right
    value = 1
  [../]
  [./inlet]
    type = DirichletBC
    variable = p
    boundary = 'right' #left
    value = 0
  [../]
[]

[Postprocessors]
  # active = 'vol perm_in perm integral_in integral_out vel_avg'
  [NumElems]
    type = NumElems
  [../] 
  [./NumDofs]
    type = NumDOFs
  [../]
  [./vol]
    type = VolumePostprocessor
    execute_on = initial
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
  [./vely_avg]
    type = ElementAverageValue
    variable = vel_y
    block = 2
  [../]
  [./velx_int]
    type = ElementIntegralVariablePostprocessor
    variable = vel_x
    block = 2
  [../]
  [./vely_int]
    type = ElementIntegralVariablePostprocessor
    variable = vel_y
    block = 2
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
[]

[Executioner]
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
    petsc_options_value = 'newtonls     fgmres     1e-2     1e-15       20       1e-9        1e-15       20           100000'
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
      vars = 'vel_x vel_y'
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
    petsc_options_value = 'gmres        asm        1E-8      1E-15        50        20         1e-8        lu                   NONZERO'
  [../]
[]

#[Problem]
#  type = FEProblem
#  material_coverage_check = false
#  kernel_coverage_check = false
#[]

[Outputs]
  file_base = perm_RCP_2D_r0005_0002_x
  csv = true
  exodus = true
  perf_graph = true
[]
