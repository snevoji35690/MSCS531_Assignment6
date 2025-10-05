from m5.objects import *

# Create the system
system = System()
system.clk_domain = SrcClockDomain(clock='1GHz', voltage_domain=VoltageDomain())
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Define 4-core MinorCPU system
system.cpu = [MinorCPU() for i in range(4)]
for cpu in system.cpu:
    cpu.icache = L1_ICache(size='32kB')
    cpu.dcache = L1_DCache(size='32kB')
    cpu.mmu = MMU()
    cpu.createThreads()

# Memory and bus setup
system.membus = SystemXBar()
for cpu in system.cpu:
    cpu.icache.connectBus(system.membus)
    cpu.dcache.connectBus(system.membus)

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8(range=system.mem_ranges[0])
system.mem_ctrl.port = system.membus.master

# Workload setup
system.workload = SEWorkload.init_compatible('daxpy_openmp')
for i, cpu in enumerate(system.cpu):
    cpu.workload = Process(cmd=['./daxpy_openmp', str(2**i)])  # vary threads
    cpu.createThreads()

root = Root(full_system=False, system=system)

m5.instantiate()
print("🚀 Running DAXPY simulation in gem5...")
exit_event = m5.simulate()
print(f"Simulation completed at tick {m5.curTick()} because {exit_event.getCause()}")
