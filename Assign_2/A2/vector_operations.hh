#ifndef __LEARNING_GEM5_VECTOR_OPERATIONS_HH__
#define __LEARNING_GEM5_VECTOR_OPERATIONS_HH__

#include "params/VectorOperations.hh"
#include "sim/sim_object.hh"

namespace gem5 
{

class VectorOperations : public SimObject
{
  private:
    void vectorCrossProduct();
    void normalizeVector();
    void vectorSubtraction();

    EventFunctionWrapper task1;
    EventFunctionWrapper task2;
    EventFunctionWrapper task3;

    Tick latency;

  public:
    VectorOperations(const VectorOperationsParams &p);

    void startup();
};

}

#endif
