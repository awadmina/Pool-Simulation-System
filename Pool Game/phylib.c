// #submittion for A1 code
// written by Mina Awad, 1175348
// Physics calculations based on data thats being recieved, and then prints the outcome

#include "phylib.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

// defining coordinates for different points on the table for new table
phylib_coord topR = {PHYLIB_TABLE_WIDTH, 0.0};
phylib_coord bottomR = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH};
phylib_coord middleR = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH};

phylib_coord topL = {0.0, 0.0};
phylib_coord middleL = {0.0, PHYLIB_TABLE_WIDTH};
phylib_coord bottomL = {0.0, PHYLIB_TABLE_LENGTH};

// function to create a new still ball object
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos)
{
    // allocating memory for the new object
    phylib_object *nObject = (phylib_object *)malloc(sizeof(phylib_object));
    if (nObject == NULL)
    {
        // return NULL if memory allocation fails
        return NULL;
    }

    // Set the object type to PHYLIB_STILL_BAL, , the still ball's number, copy the position coordinates to the still ball object
    *nObject = (phylib_object){.type = PHYLIB_STILL_BALL, .obj.still_ball.number = number, .obj.still_ball.pos = *pos};
    return nObject;
}

// function to create a new rolling ball object
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc)
{
    phylib_object *nObject = (phylib_object *)malloc(sizeof(phylib_object)); // phylib_object is the struct, new_object is the variable
    if (nObject == NULL)
    {
        return NULL;
    }

    nObject->type = PHYLIB_ROLLING_BALL;
    // set the rolling ball's number, copies acceleration, velocity, position coordinates to the rolling ball object
    nObject->obj.rolling_ball = (phylib_rolling_ball){.number = number, .pos = *pos, .vel = *vel, .acc = *acc};

    // return the newly created rolling ball object
    return nObject;
}

// function to create a new hole object
phylib_object *phylib_new_hole(phylib_coord *pos)
{
    phylib_object *nObject = (phylib_object *)malloc(sizeof(phylib_object)); // phylib_object is the struct, new_object is the variable
    if (nObject == NULL)
    {
        return NULL;
    }

    nObject->type = PHYLIB_HOLE;
    nObject->obj.hole.pos = *pos;

    return nObject;
}

// function to create a new horizontal cushion object
phylib_object *phylib_new_hcushion(double y)
{
    phylib_object *nObject = (phylib_object *)malloc(sizeof(phylib_object)); // phylib_object is the struct, new_object is the variable
    if (nObject == NULL)
    {
        return NULL;
    }

    nObject->type = PHYLIB_HCUSHION;
    nObject->obj.hcushion.y = y;

    return nObject;
}

// function to create a new vertical cushion object
phylib_object *phylib_new_vcushion(double x)
{
    phylib_object *nObject = (phylib_object *)malloc(sizeof(phylib_object)); // phylib_object is the struct, new_object is the variable
    if (nObject == NULL)
    {
        return NULL;
    }

    nObject->type = PHYLIB_VCUSHION;
    nObject->obj.vcushion.x = x;

    return nObject;
}

// function to create a new table object with various objects placed on it
phylib_table *phylib_new_table(void)
{
    phylib_table *nTable = (phylib_table *)malloc(sizeof(phylib_table)); // phylib_object is the struct, new_object is the variable
    if (nTable == NULL)
    {
        return NULL;
    }

    // restarting memory block to zero that way program doesnt carry more memory than nessessary
    memset(nTable, 0, sizeof(phylib_object));

    // elements to create new table
    nTable->object[0] = phylib_new_hcushion(0.0);
    nTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    nTable->object[2] = phylib_new_vcushion(0.0);
    nTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    // set hole coordinates
    nTable->object[4] = phylib_new_hole(&topL);
    nTable->object[5] = phylib_new_hole(&middleL);
    nTable->object[6] = phylib_new_hole(&bottomL);
    nTable->object[7] = phylib_new_hole(&topR);
    nTable->object[8] = phylib_new_hole(&middleR);
    nTable->object[9] = phylib_new_hole(&bottomR);

    // initialize data structure for table
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++)
    {
        nTable->object[i] = NULL;
    }
    return nTable;
}

// utility function to copy an object
void phylib_copy_object(phylib_object **dest, phylib_object **src)
{

    if (*src != NULL)
    {
        *dest = (phylib_object *)malloc(sizeof(phylib_object));

        if (*dest == NULL)
        {
            return;
        }
    }
    else
    {
        *dest = NULL;
    }

    memcpy(*dest, *src, sizeof(phylib_object));
}

// utility function to copy a table
phylib_table *phylib_copy_table(phylib_table *table)
{
    phylib_table *tableCopy = (phylib_table *)malloc(sizeof(phylib_table));
    if (tableCopy == NULL)
    {
        return NULL;
    }

    memcpy(tableCopy, table, sizeof(phylib_table));

    tableCopy->time = table->time;

    // copy structure and members
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            phylib_copy_object(&(tableCopy->object[i]), &(table->object[i]));
        }
    }

    return tableCopy;
}

// utility function to add an object to the table
void phylib_add_object(phylib_table *table, phylib_object *object)
{
    // find null in table, if found then add object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] == NULL)
        {
            table->object[i] = object;
            break;
        }
    }
}

// utility function to free memory allocated for the table and its objects
void phylib_free_table(phylib_table *table)
{
    // go through contents of the table, then free current object and free memory
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }
    free(table);
}

// utility function to subtract two coordinates
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{
    return (phylib_coord){c1.x - c2.x, c1.y - c2.y};
}

// utility function to calculate the length of a coordinate vector
double phylib_length(phylib_coord c)
{
    return (double)sqrt((c.x * c.x) + (c.y * c.y));
}

// utility function to calculate the dot product of two coordinates
double phylib_dot_product(phylib_coord a, phylib_coord b)
{
    return (double)(a.x * b.x) + (a.y * b.y);
}

// utility function to calculate the distance between two objects
double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{
    if (obj1->type == PHYLIB_ROLLING_BALL)
    {
        double differenceX = obj1->obj.rolling_ball.pos.x - obj2->obj.still_ball.pos.x;
        double differenceY = obj1->obj.rolling_ball.pos.y - obj2->obj.still_ball.pos.y;
        double diffHoleX = obj2->obj.hole.pos.x - obj1->obj.rolling_ball.pos.x;
        double diffHoleY = obj2->obj.hole.pos.y - obj1->obj.rolling_ball.pos.y;
        double distance = 0.0;

        switch (obj2->type)
        {
        case PHYLIB_STILL_BALL:
        case PHYLIB_ROLLING_BALL:
            distance = sqrt(((differenceX * differenceX) + (differenceY * differenceY)));
            distance -= PHYLIB_BALL_DIAMETER;
            break;

        case PHYLIB_HOLE:
            distance = sqrt(((diffHoleX * diffHoleX) + (diffHoleY * diffHoleY)));
            distance -= PHYLIB_HOLE_RADIUS;
            break;

        case PHYLIB_HCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
            break;

        case PHYLIB_VCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
            break;
        }

        return distance;
    }

    return -1.0;
}

// simulation function to update the position and velocity of a rolling ball
void phylib_roll(phylib_object *new, phylib_object *old, double time)
{

    if (new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL)
    {
        return;
    }

    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) + (0.5 * old->obj.rolling_ball.acc.x * (time * time));
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time) + (0.5 * old->obj.rolling_ball.acc.y * (time * time));

    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);

    // check if either velocity changes sign
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0.0)
    {

        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0.0)
    {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

// utility function to check if a rolling ball has stopped
unsigned char phylib_stopped(phylib_object *object)
{
    double speed = phylib_length(object->obj.rolling_ball.vel);

    if (speed < PHYLIB_VEL_EPSILON)
    {

        unsigned char number = object->obj.rolling_ball.number;
        phylib_coord pos = object->obj.rolling_ball.pos;

        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = number;
        object->obj.still_ball.pos = pos;

        return 1;
    }
    else
    {
        return 0;
    }
}

// function to handle the bouncing of two objects
void phylib_bounce(phylib_object **a, phylib_object **b)
{

    // check for invalid pointers
    if (*a == NULL || *b == NULL)
    {
        return;
    }

    phylib_object *obj_a = *a;
    phylib_object *obj_b = *b;

    switch (obj_b->type)
    {
    case PHYLIB_HCUSHION:
        obj_a->obj.rolling_ball.vel.y = -obj_a->obj.rolling_ball.vel.y;
        obj_a->obj.rolling_ball.acc.y = -obj_a->obj.rolling_ball.acc.y;
        break;
    case PHYLIB_VCUSHION:
        obj_a->obj.rolling_ball.vel.x = -obj_a->obj.rolling_ball.vel.x;
        obj_a->obj.rolling_ball.acc.x = -obj_a->obj.rolling_ball.acc.x;
        break;
    case PHYLIB_HOLE:
        free(obj_a);
        *a = NULL;
        break;
    case PHYLIB_STILL_BALL:;
        double temp_x = obj_b->obj.still_ball.pos.x;
        double temp_y = obj_b->obj.still_ball.pos.y;
        unsigned char temp_num = obj_b->obj.still_ball.number;

        obj_b->type = PHYLIB_ROLLING_BALL;
        obj_b->obj.rolling_ball.pos.x = temp_x;
        obj_b->obj.rolling_ball.pos.y = temp_y;
        obj_b->obj.rolling_ball.number = temp_num;
        obj_b->obj.rolling_ball.vel.x = 0;
        obj_b->obj.rolling_ball.vel.y = 0;
        obj_b->obj.rolling_ball.acc.x = 0;
        obj_b->obj.rolling_ball.acc.y = 0;
    case (PHYLIB_ROLLING_BALL):;

        // falling through to handle rolling ball collision
        phylib_coord r_ab = phylib_sub(obj_a->obj.rolling_ball.pos, obj_b->obj.rolling_ball.pos);

        // compute relative velocity of a with respect to b. subtract vel b from a.
        phylib_coord v_rel = phylib_sub(obj_a->obj.rolling_ball.vel, obj_b->obj.rolling_ball.vel);

        phylib_coord n;
        n.x = (r_ab.x / phylib_length(r_ab));
        n.y = (r_ab.y / phylib_length(r_ab));

        double v_rel_n = phylib_dot_product(v_rel, n);

        obj_a->obj.rolling_ball.vel.x -= (v_rel_n * n.x);
        obj_a->obj.rolling_ball.vel.y -= (v_rel_n * n.y);
        obj_b->obj.rolling_ball.vel.x += (v_rel_n * n.x);
        obj_b->obj.rolling_ball.vel.y += (v_rel_n * n.y);

        double speedA = phylib_length(obj_a->obj.rolling_ball.vel);
        double speedB = phylib_length(obj_b->obj.rolling_ball.vel);

        if (speedA > PHYLIB_VEL_EPSILON)
        {
            obj_a->obj.rolling_ball.acc.x = (-obj_a->obj.rolling_ball.vel.x) / speedA * PHYLIB_DRAG;
            obj_a->obj.rolling_ball.acc.y = (-obj_a->obj.rolling_ball.vel.y) / speedA * PHYLIB_DRAG;
        }
        if (speedB > PHYLIB_VEL_EPSILON)
        {
            obj_b->obj.rolling_ball.acc.x = (-obj_b->obj.rolling_ball.vel.x) / speedB * PHYLIB_DRAG;
            obj_b->obj.rolling_ball.acc.y = (-obj_b->obj.rolling_ball.vel.y) / speedB * PHYLIB_DRAG;
        }

        break;
    }
}

// utility function to count the number of rolling balls on the table
unsigned char phylib_rolling(phylib_table *t)
{
    unsigned char balls = 0;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (t->object[i] && t->object[i]->type == PHYLIB_ROLLING_BALL)
        {
            balls++;
        }
    }
    return balls;
}

phylib_table* phylib_segment(phylib_table* table) {
    if (table == NULL || !phylib_rolling(table)) {
        return NULL;  // Return NULL if no table or no rolling balls
    }

    double time = PHYLIB_SIM_RATE;
    phylib_table* newTable = phylib_copy_table(table);

    if (newTable != NULL) {
        int shouldExit = 0;  // Flag to indicate whether to exit the loop

        while (time < PHYLIB_MAX_TIME && !shouldExit) {
            for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
                if (newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL) {
                    phylib_roll(newTable->object[i], newTable->object[i], PHYLIB_SIM_RATE);

                    if (phylib_stopped(newTable->object[i])) {
                        shouldExit = 1;  // Set the flag to exit the loop
                        break;  // Exit the inner loop
                    }

                    for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                        if (newTable->object[j] != NULL && j != i) {
                            if (phylib_distance(newTable->object[i], newTable->object[j]) < 0.0) {
                                phylib_bounce(&(newTable->object[i]), &(newTable->object[j]));
                                shouldExit = 1;  // Set the flag to exit the loop
                                break;  // Exit the inner loop
                            }
                        }
                    }
                }
            }

            time += PHYLIB_SIM_RATE;
        }
    }

    newTable->time += time;
    return newTable;
}



//new function form assignment 2
char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object == NULL)
    {
        sprintf(string, "NULL;");
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        sprintf(string,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        sprintf(string,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        sprintf(string,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        sprintf(string,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        sprintf(string,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x);
        break;
    }
    return string;
}

