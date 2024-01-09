package mantova;

import robocode.*;
import robocode.util.*;
import static robocode.util.Utils.normalRelativeAngleDegrees;

public class TheBeast extends AdvancedRobot {
    
    private double moveAmount;
    private double previousEnergy = 100;
    private int direction = 1;
    private int gunDirection = 1;

    public void run() {
        // Configurações iniciais
        moveAmount = Math.max(getBattleFieldWidth(), getBattleFieldHeight());
        setAdjustGunForRobotTurn(true);
        setAdjustRadarForGunTurn(true);
        setTurnRadarRight(Double.POSITIVE_INFINITY);  // Rastreamento infinito
        
        while (true) {
            moveInWaves();
            chooseFirePower();
            execute();
        }
    }
    
    public void moveInWaves() {
        // Movimento oscilatório
        if (getTime() % 20 == 0) {
            direction *= -1;  // Alterna a direção
            setAhead(150 * direction);
        }
        // Movimento de parede
        if (getX() <= 100 || getY() <= 100 || getX() >= getBattleFieldWidth() - 100 || getY() >= getBattleFieldHeight() - 100) {
            direction *= -1;
        }
        setTurnRight(90);
    }
    
    public void chooseFirePower() {
        double distanceToEnemy = previousEnergy;  // Usamos energia anterior como uma métrica provisória
        if (distanceToEnemy <= 100) {
            setFire(3);
        } else if (distanceToEnemy <= 300) {
            setFire(2);
        } else {
            setFire(1);
        }
    }

    public void onScannedRobot(ScannedRobotEvent e) {
        double absoluteBearing = getHeading() + e.getBearing();
        double bearingFromGun = normalRelativeAngleDegrees(absoluteBearing - getGunHeading());
        
        // Predição de tiro
        double bulletPower = Math.min(3, getEnergy() / 6);
        double myBulletSpeed = 20 - bulletPower * 3;
        long time = (long) (e.getDistance() / myBulletSpeed);

        double futureX = e.getX() + Math.sin(e.getHeadingRadians()) * e.getVelocity() * time;
        double futureY = e.getY() + Math.cos(e.getHeadingRadians()) * e.getVelocity() * time;
        double absDeg = normalRelativeAngleDegrees(Math.toDegrees(Math.atan2(futureX - getX(), futureY - getY())));
        
        setTurnGunRight(normalRelativeAngleDegrees(absDeg - getGunHeading()));
        gunDirection = -gunDirection;
        setTurnRadarRight(2.0 * normalRelativeAngleDegrees(absoluteBearing - getRadarHeading()));
        
        double changeInEnergy = previousEnergy - e.getEnergy();
        if (changeInEnergy > 0 && changeInEnergy <= 3) {
            direction = -direction;
            setAhead((e.getDistance() / 4 + 25) * direction);
        }
        chooseFirePower();
        previousEnergy = e.getEnergy();
    }

    public void onHitByBullet(HitByBulletEvent e) {
        // Evade
        direction = -direction;
        setAhead(100 * direction);
    }

    public void onHitWall(HitWallEvent e) {
        direction = -direction;
        setBack(150 * direction);
    }

    public void onHitRobot(HitRobotEvent e) {
        direction = -direction;
        setAhead(150 * direction);
    }
}
