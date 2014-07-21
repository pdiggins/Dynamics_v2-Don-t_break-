from visual import*
import random
from particleClass import particleClass

particleList = []
tempParticleList = []
time = 0
deltat = 200000
G = 6.67E-11

def createNewParticle(input_radius, input_mParticle, input_pos, input_velocity):
    newParticle = particleClass(radius=input_radius, pos = input_pos, color = (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)))
    newParticle.trail = curve(color=newParticle.color)
    newParticle.add_Particle(input_mParticle,vector(input_velocity))
    return newParticle

def createDefinedParticle(radius, mParticle, pos, velocity):
    tempParticle = createNewParticle(radius,mParticle,pos,velocity)
    particleList.append(tempParticle)
    tempParticleList.append(tempParticle)
	
def createRandomParticles(radiusRangeStart,radiusRangeEnd, mParticleRangeStart, mParticleRangeEnd, posXStart,posXEnd,posYStart,posYEnd,posZStart,posZEnd,velocityXStart,velocityXEnd,velocityYStart,velocityYEnd,velocityZStart,velocityZEnd,numParticles):
    for x in range(0,numParticles):
        newRadius = random.uniform(radiusRangeStart,radiusRangeEnd)
        newMass = random.uniform(mParticleRangeStart, mParticleRangeEnd)
        
        newPosX = random.uniform(posXStart,posXEnd)
        newPosY = random.uniform(posYStart,posYEnd)
        newPosZ = random.uniform(posZStart,posZEnd)
        
        newPosVector = vector((newPosX/1E10,newPosY/1E10,newPosZ/1E10))
        
        newVelocityX = random.uniform(velocityXStart,velocityXEnd)
        newVelocityY = random.uniform(velocityYStart,velocityYEnd)
        newVelocityZ = random.uniform(velocityZStart,velocityZEnd)
        
        newVelocityVector = vector((newVelocityX,newVelocityY,newVelocityZ))
        tempParticle = createNewParticle(newRadius,newMass,newPosVector,newVelocityVector)
        particleList.append(tempParticle)


#sun
#Earth
createDefinedParticle(6.3781E9,5.9E24,(1.5E11,0,0),(0,3.0E4,0))
createDefinedParticle(6.955E9,2.0E30,(0,0,0),(0,0,0))
#Mercury
createDefinedParticle(2.4397E9,328.5E21,(57.91E9,0,0),(0,48.9E3,0))
#Venus
createDefinedParticle(6.045E9,4.8676E24,(1.08E11,0,0),(0,35.02E3,0))
#Mars
createDefinedParticle(3.389E9,0.64174E24,(2.279E11,0,0),(0,24.07E3,0))
#Jupiter
createDefinedParticle(71.408E9,1898.3E24,(7.785E11,0,0),(0,13.06E3,0))
#Saturn
#createDefinedParticle(60.1965E9,568.3E24,(8.907E11,0,0),(0,9.68E3,0))
#Uranus
createDefinedParticle(25.362E9,86.81E24,(2.877E12,0,0),(0,6.80E3,0))
#Neptune
createDefinedParticle(24.622E9,102.4E24,(4.503E12,0,0),(0,5.43E3,0))
#Pluto
createDefinedParticle(1.191E11,1.31E22,(4.44E12,0,0),(0,4.67E3,0))
#createDefinedParticle(6.3781E9,5.9E30,(-1.7E11,0,0),(0,-3.0E4,0))


def eulerIntegration(acceleration, particle):
    velocity = acceleration * deltat + particle.velocity
    position = velocity * deltat + particle.pos
    return position, velocity

def getGravitationalAcceleration(particle1, particle2):
    r = particle1.pos - particle2.pos
    accelerationParticle1 = -1*( G * particle2.mass * norm(r) ) / mag2(r)
    return accelerationParticle1

def getParticleAccelerationForRungeKutta(particle,index,newPos):
    acceleration = vector(0,0,0)
    counter = 0
    for i in particleList:
        if counter!= index:
            r = newPos - i.pos
            accelerationParticle1 = -1*( G * i.mass * norm(r) ) / mag2(r)
            acceleration+=accelerationParticle1
        counter+=1
    return acceleration
    
def runge_kutta(particle1,particle1Index):
    kv1 =  getParticleAccelerationForRungeKutta(particle1,particle1Index,particle1.pos)
    kv2X = particle1.pos+((deltat/2.0)*(particle1.velocity+(deltat*kv1/2.0)))           
    kv2 = getParticleAccelerationForRungeKutta(particle1,particle1Index,kv2X)
    kv3X = particle1.pos+((deltat/2.0)*(particle1.velocity+(deltat*kv2/2.0)))
    kv3 = getParticleAccelerationForRungeKutta(particle1,particle1Index,kv3X)
    kv4X = particle1.pos+((deltat)*(particle1.velocity+(deltat*kv3)))
    kv4 = getParticleAccelerationForRungeKutta(particle1,particle1Index,kv4X)
    velocity = particle1.velocity+(deltat/6.0)*(kv1+2*kv2+2*kv3+kv4)
    kp1 = particle1.velocity
    
    kp2 = particle1.velocity+getParticleAccelerationForRungeKutta(particle1,particle1Index,particle1.pos+(deltat*kp1/2.0))*deltat/2.0
    kp3 = particle1.velocity+getParticleAccelerationForRungeKutta(particle1,particle1Index,particle1.pos+(deltat*kp2/2.0))*deltat/2.0
    kp4 = particle1.velocity+getParticleAccelerationForRungeKutta(particle1,particle1Index,particle1.pos+(deltat*kp3))*deltat

    position = particle1.pos+(deltat/6.0)*(kp1+2*kp2+2*kp3+kp4)

    
    return position,velocity
											

def updateParticleUsingEulerIntegration():
    i = 0
    for i in range(0,len(particleList)):
            tempParticle = particleList[i]
            newAcceleration = vector((0,0,0))
            newPos = vector((0,0,0))
            for j in range (0,len(particleList)):
                    if(not(i==j)):
                            newAcceleration += getGravitationalAcceleration(particleList[i],particleList[j])
                            tempParticle.pos,tempParticle.velocity = eulerIntegration(newAcceleration,particleList[i])
            particleList[i].trail.append(pos=tempParticle.pos)
            particleList[i] = tempParticle

def updateParticleUsingRungeKuttaIntegration():
    i = 0
    for i in range(0,len(particleList)):
        tempParticle = particleList[i]
        newAcceleration = vector((0,0,0))
        newPos = vector((0,0,0))
        tempParticle.pos,tempParticle.velocity = runge_kutta(particleList[i],i)
        tempParticleList[i] = tempParticle
        tempParticleList[i].trail.append(pos = tempParticle.pos)
    

while(True):
    rate(1000)
    #updateParticleUsingEulerIntegration()
    updateParticleUsingRungeKuttaIntegration()
    for i in range(0,len(tempParticleList)):
        particleList[i] = tempParticleList[i]
    time = time+deltat


def get_acceleration(i, particleList):
    acceleration=(0,0,0)
    j=0
    while j<len(particleList):
        if i != j:        
            acceleration=acceleration + getGravitationalAcceleration(particleList[i], particleList[j])
        j=j+1
    return acceleration


def velocityVerlet(particleList):
    for i in range(0,len(particleList)):
        acceleration = get_acceleration(i, particleList)
        velocity = particle[i].velocity +0.5*acceleration*deltat
        particle[i].pos = particle[i].pos + velocity*deltat + 0.5*acceleration*deltat*deltat
        acceleration = get_acceleration(i, particleList)
        particle[i].velocity = velocity + 0.5*acceleration*deltat
    return particleList
